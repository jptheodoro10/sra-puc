from pydantic import BaseModel

class AlunoBase(BaseModel):
    
    matricula: str
    nome: str

class Aluno(AlunoBase):
    #api sempre nao retornando senhas por seguranca..
    id_aluno: int
    
    class Config:
        from_attributes = True 

#schemas do auth:

class Token(BaseModel):
    """Schema de resposta da rota de Login (/token)."""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Dados que guardamos dentro do Token JWT."""
    matricula: str | None = None
    aluno_id: int | None = None


#schema do submit do formulario del login:

class LoginRequest(BaseModel):
    matricula: str
    senha: str
