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

# Gerada com 'openssl rand -hex 32'
SECRET_KEY = "e75a6a2e1e3f11bb9304bdbe86039ef5e2c5071f7ed23855746e12271186704d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 # Token expira em 24 horas


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