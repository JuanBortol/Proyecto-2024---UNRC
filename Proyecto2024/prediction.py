from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

class Prediction(Base):
    __tablename__ = 'predictions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    chain_filename = Column(String, nullable=False)
    model_filename = Column(String, nullable=False)
    result = Column(String, nullable=False)  # placeholder
    date = Column(DateTime, default=datetime.now)
