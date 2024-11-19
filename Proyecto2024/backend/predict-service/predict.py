from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from gradio_client import Client, handle_file
from tensorflow.keras import layers, models
from Bio.PDB import PDBParser
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
import secrets
import os
import numpy as np
import tensorflow as tf

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": os.getenv('API_URL')}},supports_credentials=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    file_type = request.form.get('type')  # 'protein' or 'toxin'

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = secure_filename(file.filename)

        # Store filename in session
        return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200

@app.route('/submit', methods=['POST'])
def submit_files():
    if 'protein_file' not in request.files or 'toxin_file' not in request.files:
        return jsonify({'error': 'Both protein and toxin files are required'}), 400

    protein_file = request.files['protein_file']
    toxin_file = request.files['toxin_file']
    
    # Save files temporarily
    protein_filepath = f"/tmp/{protein_file.filename}"
    toxin_filepath = f"/tmp/{toxin_file.filename}"
    protein_file.save(protein_filepath)
    toxin_file.save(toxin_filepath)

    if not protein_file or not toxin_file:
        return jsonify({'error': 'Files are missing'}), 400

    try:
        # Files exist?
        if not os.path.exists(protein_filepath) or not os.path.exists(toxin_filepath):
            return jsonify({'error': 'Files not found on the server'}), 404

        # DOCKING
        docking_result = run_docking(protein_filepath, toxin_filepath)

        if docking_result.get('docking_result') != None:
            return jsonify({
                'message': 'Files submitted and saved successfully',
                'docking_result': docking_result['docking_result'],
                'docking_score': docking_result['docking_score'],
                'protein_filepath': protein_filepath,
                'toxin_filepath': toxin_filepath
            }), 200
        else:
            return jsonify({
                'error': docking_result.get('error')
            }), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/submit_model', methods=['POST'])
def submit_model():
    try:
        # Retrieve the model file, protein path, and toxin path from the request
        model_file = request.files.get('model_file')
        protein_filepath = request.form.get('protein_filepath')
        toxin_filepath = request.form.get('toxin_filepath')

        # Validate file paths
        if not protein_filepath or not os.path.exists(protein_filepath):
            return jsonify({'error': 'El archivo .pdb no se encuentra en el servidor'}), 404
        if not toxin_filepath or not os.path.exists(toxin_filepath):
            return jsonify({'error': 'El archivo .sdf no se encuentra en el servidor'}), 404

        # Handle the model file
        if model_file:
            model_filepath = f"/tmp/{model_file.filename}"
            model_file.save(model_filepath)
        else:
            # Use default model if no file is provided
            model_filepath = "mi_modelo.h5"
            if not os.path.exists(model_filepath):
                return jsonify({'error': 'El modelo predeterminado no se encuentra en el servidor'}), 404

        # Run the prediction
        degradation_result = run_predict_degradation(protein_filepath, model_filepath)
        degradation_score = float(degradation_result)

        # Determine degradation status
        degrades = 0.7 < degradation_score < 1.3

        # Respond with the results
        return jsonify({
            'message': 'Predicción de degradación completada',
            'degradation_result': degrades,
            'degradation_score': degradation_score
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Docking prediction
def run_docking(protein_filepath, toxin_filepath):

    try:

        client = Client("https://e56b06c51e1049195d7b26d043c478a0.app-space.dplink.cc/")

        # Step 1: Predict pocket using toxin file
        result_pocket = client.predict(
            ligand_file=handle_file(toxin_filepath),
            expand_size=10,
            api_name="/get_pocket_by_ligand"
        )

        # Step 2: Perform docking prediction with receptor and toxin files
        result_docking = client.predict(
            receptor_pdb=handle_file(protein_filepath),
            ligand_sdf=handle_file(toxin_filepath),
            center_x=result_pocket[0],
            center_y=result_pocket[1],
            center_z=result_pocket[2],
            size_x=result_pocket[3],
            size_y=result_pocket[4],
            size_z=result_pocket[5],
            model_version="Pocket Augmentated (Model which is more robust when the pocket is not well defined.)",
            use_unidock=True,
            task_name="Hello!!",
            api_name="/_unimol_docking_wrapper"
        )

        # Extract docking information
        a, b, c, d = result_docking

        try:
            file_path = b['value']
        except (TypeError, KeyError):
            # No docking
            return {
                'result': False,
                'docking_score': None
            }

        # Ensure the docking file exists
        if not os.path.exists(file_path):
            return {'error': 'Docking file not found'}

        # Extract docking score from the file
        with open(file_path, 'r') as file:
            for line in file:
                if line.startswith(">  <docking_score>"):
                    # Docking can be performed
                    docking_score = file.readline().strip()
                    return {
                        'docking_result': True,
                        'docking_score': docking_score
                    }
    except Exception as e:
        return {
            'error': str(e)
        }


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

if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0",port=5000)