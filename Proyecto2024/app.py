from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from database import db_session, Base, engine  # Importar db_session y Base desde database.py
from usuario import Usuario
from reporte import Reporte

app = Flask(__name__)
CORS(app) # Para fixear lo de error por puertos distintos
app.secret_key = 'your_secret_key'  # Necesario para usar flash messages

# Crear las tablas si no existen
Base.metadata.create_all(engine)

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
            existing_user = db_session.query(Usuario).filter_by(nombre=username).first()
            if existing_user:
                flash('El usuario ya existe')
            else:
                # Registrar usuario
                nuevo_usuario = Usuario(nombre=username, contraseña=password)
                db_session.add(nuevo_usuario)
                db_session.commit()
                flash('Usuario registrado con éxito')
                return redirect(url_for('login'))

    return render_template('register.html')

@app.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = db_session.query(Usuario).filter_by(nombre=username, contraseña=password).first()
    if not user:
        return jsonify({'message': 'Usuario o contraseña incorrectos'}), 400

    session['username'] = username
    return jsonify({'message': f'Bienvenido, {username}!'}), 200

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200


@app.route("/reportPage", methods=['GET', 'POST'])
def reportPage():
    if 'username' in session:
        if request.method == 'POST':
            # Obtener los datos del formulario
            incorrect_protein = request.form['incorrectProtein']
            reason = request.form['reason']
            username = session['username']

            # Verificar si los datos se están recibiendo correctamente
            print(f"Proteína incorrecta: {incorrect_protein}")
            print(f"Motivo: {reason}")
            print(f"Usuario: {username}")

            # Procesar archivo PDF (si es subido)
            pdf = request.files.get('pdfUpload')
            if pdf:
                filename = secure_filename(pdf.filename)
                pdf_path = os.path.join('uploads', filename)
                pdf.save(pdf_path)
                print(f"PDF guardado en: {pdf_path}")

            # Crear el nuevo reporte
            nuevo_reporte = Reporte(proteina=incorrect_protein, razon=reason, usuario=username)
            # Guardar el reporte en la base de datos
            db_session.add(nuevo_reporte)
            db_session.commit()

            flash('Reporte enviado con éxito.')
            return redirect(url_for('reportPage'))  # Redirigir tras el envío

        return render_template('report.html', username=session['username'])
    else:
        flash('Debes iniciar sesión para acceder a esta página.')
        return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
