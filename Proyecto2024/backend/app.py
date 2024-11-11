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
from controllers.models_controller import submit_model , run_predict_degradation

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
def submit_model_route():
    return submit_model()



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




def run_predict_degradation_route(protein_filepath, model_file):
    return run_predict_degradation(protein_filepath, model_file)


if __name__ == "__main__":
    app.run(debug=True)
