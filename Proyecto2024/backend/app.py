from flask import Flask, request, session, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from database import db_session, Base, engine  # Importar db_session y Base desde database.py
from models.user import User
from models.report import Report
from models.prediction import Prediction
from datetime import datetime
import secrets
from sqlalchemy.exc import SQLAlchemyError
import os


predict_service_url = os.getenv('VITE_PREDICT_SERVICE_URL', 'http://localhost:5000')

app = Flask(__name__, static_folder='../frontend/dist', static_url_path='/')
CORS(app, resources={r"/*": {"origins": predict_service_url}}, supports_credentials=True) # Para fixear lo de error por puertos distintos
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


@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/<path:path>', methods=['GET'])
def catch_all(path):
    # rewrite all requests from "/*" to "/index.html"
    return app.send_static_file('index.html')

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


@app.route("/register", methods=['POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if not username or not password:
            return jsonify({"message": "Todos los campos son obligatorios"}), 400
        elif password != confirm_password:
            return jsonify({"message": "Las contraseñas no coinciden"}), 400
        else:
            # User already exists?
            existing_user = db_session.query(User).filter_by(username=username).first()
            if existing_user:
                return jsonify({"message": "El usuario ya existe"}), 400
            else:
                nuevo_usuario = User(username=username, password=password)
                db_session.add(nuevo_usuario)
                db_session.commit()
                return jsonify({"message": "Usuario registrado con éxito"}), 200

    return jsonify({"message": "Método no permitido"}), 405

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
            'docking_result': prediction.docking_result,
            'docking_score': prediction.docking_score,
            'degradation_result': prediction.degradation_result,
            'degradation_score': prediction.degradation_score
        }
        for prediction in predictions
    ]
    return jsonify(predictions_data), 200

@app.route('/predictions', methods=['POST'])
def create_prediction():
    """
    Creates a new prediction entry after the /submit endpoint is invoked.
    """
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'User not logged in'}), 401

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        new_prediction = Prediction(
            user_id=user_id,
            protein_filename=data['protein_filename'],
            protein_filepath=data['protein_filepath'],
            toxin_filename=data['toxin_filename'],
            toxin_filepath=data['toxin_filepath'],
            docking_result=data['docking_result'],
            docking_score=data.get('docking_score')
        )
        db_session.add(new_prediction)
        db_session.commit()

        return jsonify({'message': 'Prediction created successfully', 'prediction_id': new_prediction.id}), 201
    except SQLAlchemyError as e:
        db_session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/predictions', methods=['PUT'])
def update_prediction():
    """
    Updates an existing prediction with degradation results after the /submit_model endpoint is invoked.
    """
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'User not logged in'}), 401

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    prediction_id = data.get('prediction_id')
    prediction = db_session.query(Prediction).filter_by(id=prediction_id, user_id=user_id).first()
    if not prediction:
        return jsonify({'error': 'Prediction not found'}), 404

    try:
        prediction.degradation_result = data.get('degradation_result')
        prediction.degradation_score = data.get('degradation_score')
        db_session.commit()

        return jsonify({'message': 'Prediction updated successfully'}), 200
    except SQLAlchemyError as e:
        db_session.rollback()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=4000)