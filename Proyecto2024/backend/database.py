from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Configuración de la base de datos
DATABASE_URL = "sqlite:///db/database.db"

# Crear el motor de la base de datos y la sesión
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
db_session = Session()

# Declaración de la base para los modelos
Base = declarative_base()
