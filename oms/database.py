from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from oms.models import Base
import os
from dotenv import load_dotenv


load_dotenv()

POSTGRES_DB_URL = os.getenv("POSTGRES_DB_URL")

engine = create_engine(POSTGRES_DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
