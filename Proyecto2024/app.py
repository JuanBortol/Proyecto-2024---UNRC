from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from database import db_session, Base, engine  # Importar db_session y Base desde database.py
from user import User
from report import Report
from prediction import Prediction
import secrets


app = Flask(__name__)
CORS(app, supports_credentials=True) # Para fixear lo de error por puertos distintos
app.secret_key = secrets.token_hex(16)  # Necesario para usar flash messages

# Crear las tablas si no existen
Base.metadata.create_all(engine)

# Set the upload folder
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

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
    file_type = request.form.get('type')

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

    chain_filename = session.get('chain_filename')
    model_filename = session.get('model_filename')
    result = 'placeholder'

    if not chain_filename or not model_filename:
        return jsonify({'error': 'Both files must be uploaded'}), 400

    # Retrieve files from the request
    chain_file = request.files.get('chain_file')
    model_file = request.files.get('model_file')

    if not chain_file or not model_file:
        return jsonify({'error': 'Files are missing'}), 400

    try:
        # Save the files
        chain_filepath = os.path.join(app.config['UPLOAD_FOLDER'], chain_filename)
        model_filepath = os.path.join(app.config['UPLOAD_FOLDER'], model_filename)
        chain_file.save(chain_filepath)
        model_file.save(model_filepath)

        # Save prediction information to the database
        prediction = Prediction(
            user_id=user_id,
            chain_filename=chain_filename,
            model_filename=model_filename,
            result=result
        )
        db_session.add(prediction)
        db_session.commit()

        # Clear filenames from session after submission
        session.pop('chain_filename', None)
        session.pop('model_filename', None)

        return jsonify({'message': 'Files submitted and saved successfully'}), 200
    except Exception as e:
        db_session.rollback()
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

@app.route("/reportPage", methods=['GET', 'POST'])
def reportPage():
    if 'user_id' in session:
        user_id = session['user_id']
        if request.method == 'POST':
            user = db_session.query(User).filter_by(id=user_id.first())
            # Obtener los datos del formulario
            incorrect_chain = request.form['incorrectProtein']
            reason = request.form['reason']
            username = user.username

            # Verificar si los datos se están recibiendo correctamente
            print(f"Cadena incorrecta: {incorrect_chain}")
            print(f"Motivo: {reason}")
            print(f"User: {username}")

            # Procesar archivo PDF (si es subido)
            pdf = request.files.get('pdfUpload')
            if pdf:
                filename = secure_filename(pdf.filename)
                pdf_path = os.path.join('uploads', filename)
                pdf.save(pdf_path)
                print(f"PDF guardado en: {pdf_path}")

            # Crear el nuevo reporte
            new_report = Report(chain=incorrect_chain, reason=reason, user_id=user_id)
            # Guardar el reporte en la base de datos
            db_session.add(new_report)
            db_session.commit()

            flash('Reporte enviado con éxito.')
            return redirect(url_for('reportPage'))  # Redirigir tras el envío

        return render_template('report.html', username=username)
    else:
        flash('Debes iniciar sesión para acceder a esta página.')
        return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)