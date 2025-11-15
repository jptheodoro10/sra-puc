from sqlalchemy.orm import Session
import models
import schemas
# O auth não é necessário aqui, pois não estamos criando senhas

def get_aluno_by_id(db: Session, aluno_id: int):
    """Busca aluno pelo ID."""
    return db.query(models.Aluno).filter(models.Aluno.id_aluno == aluno_id).first()

def get_aluno_by_matricula(db: Session, matricula: str):
    """Busca aluno pela Matrícula (usado no login)."""
    return db.query(models.Aluno).filter(models.Aluno.matricula == matricula).first()

# --- Funções das próximas rotas ---

# (Ainda não precisamos, mas elas virão aqui)
# def get_disciplinas(db: Session): ...
# def get_opcoes_preferencia(db: Session): ...
# def get_professor_profile_vector(db: Session, professor_id: int, disciplina_id: int): ...
# def get_aluno_preference_vector(db: Session, aluno_id: int): ...