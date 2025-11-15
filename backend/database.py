from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

DATABASE_URL = 'postgresql://neondb_owner:npg_H7wacAy1BqOE@ep-flat-firefly-acycnx2r.sa-east-1.aws.neon.tech/sra_example2_alchemy?sslmode=require&channel_binding=require'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit = False, autoflush= False, bind= engine)
Base = declarative_base()

def get_db():
    db = SessionLocal() # incializa a sessao
    try:
        yield db  # fornece a sessão para a requisição
    finally:
        db.close() # fecha a sessão ao final da requisição