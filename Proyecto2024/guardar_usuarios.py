from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Crear la base de datos en SQLite
engine = create_engine('sqlite:///usuarios.db', echo=True)
Base = declarative_base()


# Definir el modelo de la tabla de usuarios
class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    correo = Column(String)
    contraseña = Column(String)


# Crear la tabla
Base.metadata.create_all(engine)

# Crear una sesión
Session = sessionmaker(bind=engine)
session = Session()
