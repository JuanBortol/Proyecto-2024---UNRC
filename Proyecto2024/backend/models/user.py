from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base  # Importar Base desde database.py

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    reports = relationship("Report", back_populates="user")
