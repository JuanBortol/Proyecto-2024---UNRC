import pytest
from flask import session
from app import app, db_session, save_files, validate_session_and_user, validate_files_in_session, process_docking_and_save
from models.user import User
from models.prediction import Prediction
import os
from io import BytesIO


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['UPLOAD_FOLDER'] = 'test_uploads/'
    with app.test_client() as client:
        with app.app_context():
            # Crear base de datos en memoria
            db_session.bind = 'sqlite:///:memory:'
            db_session.close()
        yield client


@pytest.fixture
def setup_user():
    """Crea un usuario para las pruebas."""
    user = User(username="test_user", email="test@example.com")
    db_session.add(user)
    db_session.commit()
    return user


def test_validate_session_and_user(client, setup_user):
    with client.session_transaction() as sess:
        sess['user_id'] = setup_user.id

    result = validate_session_and_user()
    assert result['user_id'] == setup_user.id


def test_validate_session_and_user_no_user(client):
    with client.session_transaction() as sess:
        sess['user_id'] = 999  # ID que no existe

    result = validate_session_and_user()
    assert 'error' in result
    assert result['error'] == 'User not found'


def test_validate_files_in_session(client):
    with client.session_transaction() as sess:
        sess['protein_filename'] = 'protein.pdb'
        sess['toxin_filename'] = 'toxin.pdb'

    result = validate_files_in_session()
    assert result['protein_filename'] == 'protein.pdb'
    assert result['toxin_filename'] == 'toxin.pdb'


def test_validate_files_in_session_missing_files(client):
    with client.session_transaction() as sess:
        sess['protein_filename'] = 'protein.pdb'

    result = validate_files_in_session()
    assert 'error' in result
    assert result['error'] == 'Both files must be uploaded'


def test_save_files(client, setup_user, tmpdir):
    app.config['UPLOAD_FOLDER'] = str(tmpdir)
    protein_file = BytesIO(b"protein content")
    toxin_file = BytesIO(b"toxin content")
    protein_filename = 'protein.pdb'
    toxin_filename = 'toxin.pdb'

    protein_filepath, toxin_filepath = save_files(
        protein_file=protein_file,
        toxin_file=toxin_file,
        protein_filename=protein_filename,
        toxin_filename=toxin_filename,
        user_id=setup_user.id
    )

    assert os.path.exists(protein_filepath)
    assert os.path.exists(toxin_filepath)


def test_process_docking_and_save(client, setup_user, tmpdir, mocker):
    # Mockear la función `run_docking`
    mocker.patch('app.run_docking', return_value={
        'docking_result': 'success',
        'docking_score': 0.85
    })

    protein_filepath = os.path.join(str(tmpdir), 'protein.pdb')
    toxin_filepath = os.path.join(str(tmpdir), 'toxin.pdb')

    with open(protein_filepath, 'w') as f:
        f.write('protein content')
    with open(toxin_filepath, 'w') as f:
        f.write('toxin content')

    response, status_code = process_docking_and_save(
        protein_filepath=protein_filepath,
        toxin_filepath=toxin_filepath,
        protein_filename='protein.pdb',
        toxin_filename='toxin.pdb',
        user_id=setup_user.id
    )

    assert status_code == 200
    assert response['message'] == 'Files submitted and saved successfully'
    assert 'docking_result' in response
    assert response['docking_result'] == 'success'

    # Verificar si la predicción se guarda en la base de datos
    prediction = db_session.query(Prediction).filter_by(user_id=setup_user.id).first()
    assert prediction is not None
    assert prediction.docking_result == 'success'
    assert prediction.docking_score == 0.85
