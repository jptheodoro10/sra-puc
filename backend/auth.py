import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import crud
import models
import schemas
from database import SessionLocal, get_db

# hashing e senha com bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)



def authenticate_user(db: Session, matricula: str, password: str):
    """verifica a matrícula e a senha no banco de dados. Função chamada pela rota de login.
    """
   
    aluno = crud.get_aluno_by_matricula(db, matricula=matricula)
    
    if not aluno:
        return None 
    
   
    if not verify_password(password, aluno.hashed_password):
        return None
    
   
    return aluno


# Token JWT:

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY environment variable is not set")

ALGORITHM = "HS256"

_token_expire_minutes = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
try:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(_token_expire_minutes) if _token_expire_minutes else 60 * 24  # 24h default
except ValueError as exc:
    raise RuntimeError("ACCESS_TOKEN_EXPIRE_MINUTES must be an integer") from exc


# diz ao FastAPI que a rota de login é /login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    
    #Cria um novo Token JWT pro usuario
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# dependência para rota protegidas:
#a funcao abaixo eh uma dependencia para qualquer rota que necessite que o aluno esteja logado para acessar, como 'obter recomendacao'. Rotas desprotegidas como 'fazer login' nao levam ela, pois nao requerem um usuario pre-autenticado.

async def get_current_aluno(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Qualquer rota que precisar desta dependecia vai ter que:
    1. Exigir um Token no Header.
    2. Decodificar o Token.
    3. Retornar o objeto 'Aluno' do banco.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # O "subject" do token é a matrícula
        matricula: str = payload.get("sub") 
        aluno_id: int = payload.get("aluno_id")
        
        if matricula is None or aluno_id is None:
            raise credentials_exception
        
        
        token_data = schemas.TokenData(matricula=matricula, aluno_id=aluno_id)
        
    except JWTError:
        raise credentials_exception
    
   
    aluno = crud.get_aluno_by_id(db, aluno_id=token_data.aluno_id)
    
    if aluno is None:   
        raise credentials_exception
    return aluno
