from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from database import db_session, Base, engine  # Importar db_session y Base desde database.py
from gradio_client import Client, handle_file
from models.user import User
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
from controllers.user_controller import register, login, logout
from controllers.prediction_controller import submit_files, submit_report, get_user_predictions

app = Flask(__name__)
CORS(app, supports_credentials=True) # Para fixear lo de error por puertos distintos
app.secret_key = secrets.token_hex(16)  # Necesario para usar flash messages

# Crear las tablas si no existen
Base.metadata.create_all(engine)

# Set the upload folder
UPLOAD_FOLDER = 'uploads/'
REPORT_FOLDER = os.path.join(UPLOAD_FOLDER, 'reports')


default_model_filename = 'mi_modelo.h5'
default_model_filepath = './mi_modelo.h5'
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
def submit_files_route():
    return submit_files()


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
        degradation_score = float(degradation_result)

        degrades = degradation_score > 0.7 and degradation_score < 1.30

        # Update degradation result and score IN DATABASE
        prediction.degradation_result = degrades
        prediction.degradation_score = degradation_score
        db_session.commit()

        return jsonify({
            'message': 'Predicción de degradación completada',
            'degradation_result': degrades,
            'degradation_score': degradation_score
        }), 200

    except Exception as e:
        db_session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route("/register", methods=['POST'])
def register_route():
    return register()

@app.route("/login", methods=['POST'])
def login_route():
    return login()

@app.route('/logout', methods=['POST'])
def logout_route():
    return logout()

@app.route("/submit_report", methods=['POST'])
def submit_report_route():
    return submit_report()

# Returns all predictions made by current user
@app.route('/predictions', methods=['GET'])
def get_user_predictions_route():
    return get_user_predictions()




def run_predict_degradation(protein_filepath, model_file):
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


    model = tf.keras.models.load_model(model_file)

    prediction_score = predict_protein(protein_filepath, model)

    return prediction_score


if __name__ == "__main__":
    app.run(debug=True)
