from flask import request, jsonify, session
from database import db_session
from models.user import User

def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    if not username or not password:
        return jsonify({"message": "Todos los campos son obligatorios"}), 400
    elif password != confirm_password:
        return jsonify({"message": "Las contraseñas no coinciden"}), 400
    
    existing_user = db_session.query(User).filter_by(username=username).first()
    if existing_user:
        return jsonify({"message": "El usuario ya existe"}), 400

    nuevo_usuario = User(username=username, password=password)
    db_session.add(nuevo_usuario)
    db_session.commit()
    return jsonify({"message": "Usuario registrado con éxito"}), 200

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
    return jsonify({"user_id": user.id, "username": user.username}), 200

def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200
