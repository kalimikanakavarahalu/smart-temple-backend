from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Get DB URL from env, fallback to a local default if missing
SQLALCHEMY_DATABASE_URL = os.getenv("DB_URL", "postgresql://temple_admin:temple_secure@localhost:5432/smart_temple")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
