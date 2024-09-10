from flask import Flask, render_template, request, redirect, url_for, flash, session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from modelo import Usuario  # Asegúrate de tener el archivo modelo.py con el modelo definido

# Configuración de la base de datos
DATABASE_URL = 'sqlite:///usuarios.db'

engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)

# Crear una sesión
db_session = Session()

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necesario para usar flash messages

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

@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validación de credenciales
        user = db_session.query(Usuario).filter_by(nombre=username, contraseña=password).first()
        if not user:
            flash('Usuario o contraseña incorrectos')
        else:
            session['username'] = username
            flash(f'Bienvenido, {username}!')
            return redirect(url_for('home'))

    return render_template('login.html')

@app.route("/logout")
def logout():
    session.pop('username', None)
    flash('Has cerrado sesión')
    return redirect(url_for('home'))

@app.route("/home", methods=['GET', 'POST'])
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    else:
        flash('Debes iniciar sesión para acceder a esta página.')
        return redirect(url_for('login'))

@app.route("/reportPage", methods=['GET','POST'])
def reportPage():
    if'username' in session:
        return render_template('report.html', username=session['username'])
    else:
        flash('Debes iniciar session para acceder a esta pagina.')
        return redirect(url_for('login'))


if __name__ == "__main__":
    # Crear tablas si no existen
    Base.metadata.create_all(engine)
    app.run(debug=True)
