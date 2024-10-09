from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from database import Base

class Prediction(Base):
    __tablename__ = 'predictions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    protein_filename = Column(String, nullable=False)
    protein_filepath = Column(String, nullable=False)
    toxin_filename = Column(String, nullable=False)
    toxin_filepath = Column(String, nullable=False)
    result = Column(Boolean, nullable=False)
    docking_score = Column(Integer)
    date = Column(DateTime, default=datetime.now)