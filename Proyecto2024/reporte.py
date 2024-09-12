from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Reporte(Base):
    __tablename__ = 'reportes'

    id = Column(Integer, primary_key=True, autoincrement=True)  # Agrega un id para el reporte
    proteina = Column(String, nullable=False)
    razon = Column(String, nullable=False)
    usuario = Column(String, ForeignKey('usuarios.nombre'))

    usuario_rel = relationship("Usuario", back_populates="reportes")
