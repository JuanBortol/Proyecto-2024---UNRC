import secrets
from flask import  Flask, request, jsonify, session
from flask_cors import CORS
import tensorflow as tf
from models.prediction import Prediction
from database import db_session  
from models.user import User
from werkzeug.utils import secure_filename  
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
from Bio.PDB import PDBParser
import os

app = Flask(__name__)
CORS(app, supports_credentials=True) # Para fixear lo de error por puertos distintos
app.secret_key = secrets.token_hex(16) 


default_model_filename = 'mi_modelo.h5'
default_model_filepath = './mi_modelo.h5'

# Set the upload folder
UPLOAD_FOLDER = "Proyecto2024/backend/uploads"
REPORT_FOLDER = os.path.join(UPLOAD_FOLDER, "reports")

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['REPORT_FOLDER'] = REPORT_FOLDER

# Create the folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

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
