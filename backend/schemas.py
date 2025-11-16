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
    # 'curso' e 'periodo' não são usados no vetor, mas é bom receber
    curso: str
    periodo: str
    
    # As 4 categorias de preferência
    formaLecionar: str
    formaAvaliar: str
    ritmoAula: str
    incentivo: str # No frontend é 'incentivo', no form é 'Participação'
    
    # As 4 importâncias
    formaLecionarImportancia: int
    formaAvaliarImportancia: int
    ritmoAulaImportancia: int
    incentivoImportancia: int


class PreferenciaItem(BaseModel):
    id_preferencia: int
    coluna: str
    peso: int
    
    class Config:
        from_attributes = True


class PerfilPreferencias(BaseModel):
    id_perfil: int
    aluno_id: int
    preferencias: list[PreferenciaItem]

    class Config:
        from_attributes = True


class ProfessorComSimilaridade(BaseModel):
    id_professor: int
    nome: str
    similaridade: float
