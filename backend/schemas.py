from pydantic import BaseModel
from typing import List

class AlunoBase(BaseModel):
    
    matricula: str
    nome: str

class Aluno(AlunoBase):
    id_aluno: int
    
    class Config:
        from_attributes = True 

#schemas do auth:

class Token(BaseModel):
    """Schema de resposta da rota de Login (/token)."""
    access_token: str
    token_type: str
    has_profile: bool
    nome: str

class TokenData(BaseModel):
    """Dados que guardamos dentro do Token JWT."""
    matricula: str | None = None
    aluno_id: int | None = None


#schema do submit do formulario del login:

class LoginRequest(BaseModel):
    matricula: str
    senha: str

class PerfilFrontend(BaseModel):
    curso: str
    periodo: str
    
    formaLecionar: str
    formaAvaliar: str
    ritmoAula: str
    incentivo: str 
    
    formaLecionarImportancia: int
    formaAvaliarImportancia: int
    ritmoAulaImportancia: int
    incentivoImportancia: int

class OpcaoSchemaHelper(BaseModel):
    id_opcao: int
    nome: str
    coluna_mapeada: str
    
    class Config:
        from_attributes = True

class PreferenciaItem(BaseModel):
    id_preferencia: int
    opcao: OpcaoSchemaHelper
    peso: int
    
    class Config:
        from_attributes = True


class PerfilPreferencias(BaseModel):
    #resposta da rota /recomendaoes
    id_perfil: int
    aluno_id: int
    preferencias: list[PreferenciaItem]

    class Config:
        from_attributes = True


class ProfessorComSimilaridade(BaseModel):
    id_professor: int
    nome: str
    similaridade: float
    estrelas: float

    class Config:
        from_attributes = True

class Disciplina(BaseModel):
    id_disciplina: int
    nome: str
    
    class Config:
        from_attributes = True
