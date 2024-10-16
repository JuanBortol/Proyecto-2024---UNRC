from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from database import db_session, Base, engine  # Importar db_session y Base desde database.py
from gradio_client import Client, handle_file
from models.user import User
from models.report import Report
from models.prediction import Prediction
from datetime import datetime
from tensorflow.keras import layers, models
from Bio.PDB import PDBParser
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
import secrets
import os
import numpy as np
import tensorflow as tf


app = Flask(__name__)
CORS(app, supports_credentials=True) # Para fixear lo de error por puertos distintos
app.secret_key = secrets.token_hex(16)  # Necesario para usar flash messages

# Crear las tablas si no existen
Base.metadata.create_all(engine)

# Set the upload folder
UPLOAD_FOLDER = 'uploads/'
REPORT_FOLDER = os.path.join(UPLOAD_FOLDER, 'reports')


default_model_filename = 'mi_modelo.h5'
default_model_filepath = os.path.join(UPLOAD_FOLDER, 'models', 'default', default_model_filename)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['REPORT_FOLDER'] = REPORT_FOLDER

# Create the folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Returns current user for AppContext no borrar pls
@app.route('/@me', methods=['GET'])
def get_current_user():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"id": None, "username": None})
    
    user = db_session.query(User).filter_by(id=user_id).first()
    if user:
        return jsonify({
            "id": user_id,
            "username": user.username
        })
    else:
        return jsonify({"id": None, "username": None})

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'user_id' not in session:
        return 'User not logged in', 401
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    file_type = request.form.get('type')  # 'protein' or 'toxin'

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = secure_filename(file.filename)

        # Store filename in session
        session[f'{file_type}_filename'] = filename
        return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200


@app.route('/submit', methods=['POST'])
def submit_files():
    if 'user_id' not in session:
        return jsonify({'error': 'User not logged in'}), 401

    user_id = session['user_id']
    user = db_session.query(User).filter_by(id=user_id).first()
    
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Get file names from session
    protein_filename = session.get('protein_filename')
    toxin_filename = session.get('toxin_filename')

    if not protein_filename or not toxin_filename:
        return jsonify({'error': 'Both files must be uploaded'}), 400
    
    # Retrieve files from the request
    protein_file = request.files.get('protein_file')
    toxin_file = request.files.get('toxin_file')

    if not protein_file or not toxin_file:
        return jsonify({'error': 'Files are missing'}), 400

    try:
        # Set up the folder path
        current_date = datetime.utcnow().strftime("%Y_%m_%d")
        timestamp = datetime.utcnow().strftime("%H%M%S")
        protein_name = os.path.splitext(protein_filename)[0]  # Get rid of extension
        
        # path: uploads/predictions/user_{user_id}/YYYY_MM_DD/{protein_name}_{timestamp}
        user_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'predictions', f'user_{user_id}', current_date)
        prediction_folder = os.path.join(user_folder, f'{protein_name}_{timestamp}')
        
        # Create the directories if they don't exist
        os.makedirs(prediction_folder, exist_ok=True)
        
        # File paths
        protein_filepath = os.path.join(prediction_folder, protein_filename)
        toxin_filepath = os.path.join(prediction_folder, toxin_filename)
        
        # Save the files
        protein_file.save(protein_filepath)
        toxin_file.save(toxin_filepath)

        # Files exist?
        if not os.path.exists(protein_filepath) or not os.path.exists(toxin_filepath):
            return jsonify({'error': 'Files not found on the server'}), 404

        # DOCKING
        docking_result = run_docking(protein_filepath, toxin_filepath)

        if docking_result.get('result') != None:
            # Save prediction
            prediction = Prediction(
                user_id=user_id,
                protein_filename=protein_filename,
                protein_filepath=protein_filepath,
                toxin_filename=toxin_filename,
                toxin_filepath=toxin_filepath,
                result=docking_result['result'],
                docking_score=docking_result['docking_score']
            )
            db_session.add(prediction)
            db_session.commit()

            # Clear session filenames
            session.pop('protein_filename', None)
            session.pop('toxin_filename', None)

            return jsonify({
                'message': 'Files submitted and saved successfully',
                'result': docking_result['result'],
                'docking_score': docking_result['docking_score'],
                'protein': protein_filename,
                'toxin': toxin_filename,
                'prediction_id': prediction.id
            }), 200
        else:
            return jsonify({
                'error': docking_result.get('error')
            }), 400
    except Exception as e:
        db_session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/submit_model', methods=['POST'])
def submit_model():
    if 'user_id' not in session:
        return jsonify({'error': 'Usuario no logeado'}), 401

    user_id = session['user_id']
    user = db_session.query(User).filter_by(id=user_id).first()

    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    # Get model file and prediction id from request
    model_file = request.files.get('model_file')
    prediction_id = request.form.get('prediction_id')

    if not prediction_id:
        return jsonify({'error': 'Fallo al proveer ID de Predicción'}), 400

    # Retrieve the Prediction object
    prediction = db_session.query(Prediction).filter_by(id=prediction_id, user_id=session['user_id']).first()

    if not prediction:
        return jsonify({'error': 'No se ha encontrado la predicción'}), 404

    # Models folder
    models_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'models')
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)

    if not model_file:
        # Si no se proporciona un archivo, usa el modelo predeterminado
        model_filepath = default_model_filepath
    else:
        model_filename = model_file.filename
        model_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'models', model_filename)
        model_file.save(model_filepath)

    # Filepaths for both the protein and toxin    
    protein_filepath = prediction.protein_filepath
    toxin_filepath = prediction.toxin_filepath

    if not os.path.exists(protein_filepath) or not os.path.exists(toxin_filepath):
        return jsonify({'error': 'El archivo .pdb o .sdf no se encuentran en el servidor'}), 404

    try:
        degradation_result = run_predict_degradation(protein_filepath, model_filepath)

        d_r = float(degradation_result)

        return jsonify({
            'message': 'Predicción de degradación completada',
            'degradation_result': d_r
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Validaciones simples
        if not username or not password:
            flash('Todos los campos son obligatorios')
        elif password != confirm_password:
            flash('Las contraseñas no coinciden')
        else:
            # Verificar si el usuario ya existe
            existing_user = db_session.query(User).filter_by(username=username).first()
            if existing_user:
                flash('El usuario ya existe')
            else:
                # Registrar usuario
                nuevo_usuario = User(username=username, password=password)
                db_session.add(nuevo_usuario)
                db_session.commit()
                flash('Usuario registrado con éxito')
                return redirect(url_for('login'))

    return render_template('register.html')

@app.route("/login", methods=['POST'])
def login():
    if 'user_id' in session:
        return jsonify({'message': 'User already logged in'}), 200
    
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = db_session.query(User).filter_by(username=username, password=password).first()

    if not user:
        return jsonify({'message': 'Usuario o contraseña incorrectos'}), 400

    session['user_id'] = user.id
    session['username'] = user.username

    return jsonify({
        "user_id": user.id,
        "username": user.username
        }), 200

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route("/submit_report", methods=['POST'])
def submit_report():
    if 'user_id' in session:
        user_id = session['user_id']
        user = db_session.query(User).filter_by(id=user_id).first()
        if not user:
            return jsonify({"message": "User not found"}), 404

        # Get files and reason
        protein_file = request.files.get('protein_file')
        toxin_file = request.files.get('toxin_file')
        pdf_file = request.files.get('pdf_file')
        reason = request.form.get('reason')

        if not protein_file or not reason:
            return jsonify({"message": "protein file and reason are required"}), 400

        current_date = datetime.utcnow().strftime("%Y-%m-%d")  # YYYY-MM-DD
        protein_filename = secure_filename(protein_file.filename)
        protein_name, _ = os.path.splitext(protein_filename)  # Gets rid of file extension
        toxin_filename = secure_filename(toxin_file.filename)
        toxin_name, _ = os.path.splitext(toxin_filename)  # Gets rid of file extension
        timestamp = datetime.utcnow().strftime("%H%M%S")
        report_folder_name = f"{protein_name}_{timestamp}"

        # User folder
        user_folder = os.path.join(REPORT_FOLDER, f"user_{user_id}")
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)

        # Date folder
        date_folder = os.path.join(user_folder, current_date)
        if not os.path.exists(date_folder):
            os.makedirs(date_folder)

        # Report folder
        report_folder = os.path.join(date_folder, report_folder_name)
        if not os.path.exists(report_folder):
            os.makedirs(report_folder)

        # protein & toxin file handlers
        protein_path = os.path.join(report_folder, protein_filename)
        protein_file.save(protein_path)
        toxin_path = os.path.join(report_folder, toxin_filename)
        toxin_file.save(toxin_path)

        # PDF File handler
        pdf_filename = None
        if pdf_file:
            pdf_filename = secure_filename(pdf_file.filename)
            pdf_path = os.path.join(report_folder, pdf_filename)
            pdf_file.save(pdf_path)

        # Creates report
        new_report = Report(
            protein=protein_filename,
            toxin=toxin_filename,
            pdf=pdf_filename, 
            reason=reason, 
            user_id=user_id
        )
        db_session.add(new_report)
        db_session.commit()

        return jsonify({"message": "Report successfully submitted"}), 200
    else:
        return jsonify({"error": "Unauthorized"}), 401

# Returns all predictions made by current user
@app.route('/predictions', methods=['GET'])
def get_user_predictions():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'User not logged in'}), 401
    predictions = db_session.query(Prediction).filter_by(user_id=user_id).all()
    predictions_data = [
        {
            'date': prediction.date.strftime('%d/%m/%y'),
            'protein_filename': prediction.protein_filename,
            'toxin_filename': prediction.toxin_filename,
            'result': prediction.result,
            'docking_score': prediction.docking_score
        }
        for prediction in predictions
    ]
    return jsonify(predictions_data), 200

# Docking prediction
def run_docking(protein_filepath, toxin_filepath):
    return {
        'result': True,
        'docking_score': -1.23456789
    }
    # Commented for testing purposes
    # try:
        # Initialize Gradio client
        # client = Client("https://f57a2f557b098c43f11ab969efe1504b.app-space.dplink.cc/")
        
        # # Step 1: Predict pocket using toxin file
        # result_pocket = client.predict(
        #     ligand_file=handle_file(toxin_filepath),
        #     expand_size=10,
        #     api_name="/get_pocket_by_ligand"
        # )
        
        # # Step 2: Perform docking prediction with receptor and toxin files
        # result_docking = client.predict(
        #     receptor_pdb=handle_file(protein_filepath),
        #     ligand_sdf=handle_file(toxin_filepath),
        #     center_x=result_pocket[0],
        #     center_y=result_pocket[1],
        #     center_z=result_pocket[2],
        #     size_x=result_pocket[3],
        #     size_y=result_pocket[4],
        #     size_z=result_pocket[5],
        #     model_version="Pocket Augmentated (Model which is more robust when the pocket is not well defined.)",
        #     use_unidock=True,
        #     task_name="Hello!!",
        #     api_name="/_unimol_docking_wrapper"
        # )

        # # Extract docking information
        # a, b, c, d = result_docking
        
        # try:
        #     file_path = b['value']
        # except (TypeError, KeyError):
        #     # No docking
        #     return {
        #         'result': False,
        #         'docking_score': None
        #     }

    #     # Ensure the docking file exists
    #     if not os.path.exists(file_path):
    #         return {'error': 'Docking file not found'}

    #     # Extract docking score from the file
    #     with open(file_path, 'r') as file:
    #         for line in file:
    #             if line.startswith(">  <docking_score>"):
    #                 # Docking can be performed
    #                 docking_score = file.readline().strip()
    #                 return {
    #                     'result': True,
    #                     'docking_score': docking_score
    #                 }
    # except Exception as e:
    #     return {
    #         'error': str(e)
    #     }


def run_predict_degradation(protein_filepath, model_filepath):
    def pdb_to_numeric_padded(pdb_files, max_len=1000):
        sequences = []
        for pdb_file in pdb_files:
            coords = pdb_to_numeric(pdb_file)
            sequences.append(coords)

        # Padeamos las secuencias para que todas tengan el mismo número de átomos, con 3 columnas (x, y, z)
        padded_sequences = pad_sequences(sequences, maxlen=max_len, padding='post', dtype='float32')
        return padded_sequences

    def pdb_to_numeric(pdb_file):
        parser = PDBParser()
        structure = parser.get_structure('protein', pdb_file)

        atom_coords = []
        for model in structure:
            for chain in model:
                for residue in chain:
                    for atom in residue:
                        atom_coords.append(atom.coord)  # Coordenadas (x, y, z)

        # Convertir a un array numpy
        atom_coords = np.array(atom_coords)

        # Normalizar las coordenadas
        atom_coords = (atom_coords - np.mean(atom_coords, axis=0)) / np.std(atom_coords, axis=0)

        return atom_coords

    # Función para realizar predicción sobre una proteína PDB
    def predict_protein(protein, modelo_keras, max_len=1000):
        # Convertir el archivo PDB en una representación numérica
        protein_numeric = pdb_to_numeric_padded([protein], max_len=max_len)

        # Realizar la predicción
        prediction = modelo_keras.predict(protein_numeric)

        # Retornar el valor de la predicción
        return prediction[0][0]

    model = tf.keras.models.load_model(model_filepath)

    prediction_score = predict_protein(protein_filepath, model)

    return prediction_score


if __name__ == "__main__":
    app.run(debug=True)
