from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base  # Importar Base desde database.py

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nombre = Column(String, unique=True, nullable=False)
    contraseña = Column(String, nullable=False)

    reportes = relationship("Reporte", back_populates="usuario_rel")
