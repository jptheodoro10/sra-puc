import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# Load environment variables from a .env file if present (local dev convenience).
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Fails fast to avoid accidentally using a hardcoded/incorrect URL.
    raise RuntimeError("DATABASE_URL environment variable is not set")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit = False, autoflush= False, bind= engine)
Base = declarative_base()

def get_db():
    db = SessionLocal() # incializa a sessao
    try:
        yield db  # fornece a sessão para a requisição
    finally:
        db.close() # fecha a sessão ao final da requisição
