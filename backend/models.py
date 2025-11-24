from sqlalchemy import Column, Integer, String, Float, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base  # Importa o Base do seu arquivo database.py

# --- TABELAS CENTRAIS: ALUNO, PROFESSOR, DISCIPLINA ---

class Aluno(Base):
    __tablename__ = 'alunos'
    
    id_aluno = Column(Integer, primary_key=True)
    matricula = Column(String(50), nullable=False, unique=True, index=True)
    nome = Column(String(100), nullable=False)
    hashed_password = Column(String(255), nullable=False) 
    
    
    # Relacionamento 1-para-1 com PerfilPreferencias
    perfil_preferencias = relationship('PerfilPreferencias', back_populates='aluno', uselist=False, cascade="all, delete-orphan")
    
    # Relacionamento 1-para-N com Avaliacao
    avaliacoes = relationship('Avaliacao', back_populates='aluno')

class Professor(Base):
    __tablename__ = 'professores'
    
    id_professor = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    
    # Relacionamento 1-para-N com Turma
    turmas = relationship('Turma', back_populates='professor')

class Curso(Base):
    __tablename__ = 'cursos'
    id_curso = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False, unique=True)
    
    disciplinas = relationship('Disciplina', back_populates='curso')

class Disciplina(Base):
    __tablename__ = 'disciplinas'
    
    id_disciplina = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False, unique=True)
    curso_id = Column(Integer, ForeignKey('cursos.id_curso'), nullable=True) # Opcional
    
    curso = relationship('Curso', back_populates='disciplinas')
    turmas = relationship('Turma', back_populates='disciplina')

class Turma(Base):
    __tablename__ = 'turmas'
    
    id_turma = Column(Integer, primary_key=True)
    nome_turma = Column(String(50), nullable=False) # ex: "3WA", "3WB"
    semestre = Column(String(20), nullable=False) # ex: "2025.1"
    
    professor_id = Column(Integer, ForeignKey('professores.id_professor'), nullable=False)
    disciplina_id = Column(Integer, ForeignKey('disciplinas.id_disciplina'), nullable=False)
    
    professor = relationship('Professor', back_populates='turmas')
    disciplina = relationship('Disciplina', back_populates='turmas')
    
    avaliacoes = relationship('Avaliacao', back_populates='turma')

class Avaliacao(Base):
    
    #O backend usará (AVG) desses dados para criar o "perfil do professor".
   
    __tablename__ = 'avaliacoes'
    
    id_avaliacao = Column(Integer, primary_key=True)
    semestre = Column(String(20), nullable=False) 
    
    turma_id = Column(Integer, ForeignKey('turmas.id_turma'), nullable=False)
    aluno_id = Column(Integer, ForeignKey('alunos.id_aluno'), nullable=False)
    
    turma = relationship('Turma', back_populates='avaliacoes')
    aluno = relationship('Aluno', back_populates='avaliacoes')
    
    slide = Column(Integer, nullable=False, default=0)
    quadro = Column(Integer, nullable=False, default=0)
    velocidade_aula = Column(Integer, nullable=False, default=0)
    provas = Column(Integer, nullable=False, default=0)
    trabalhos = Column(Integer, nullable=False, default=0)
    projetos = Column(Integer, nullable=False, default=0)
    interacao = Column(Integer, nullable=False, default=0)
    
    __table_args__ = (
        UniqueConstraint('aluno_id', 'turma_id', name='uq_aluno_turma'),
        CheckConstraint('slide >= 0 AND slide <= 7', name='check_aval_slide'),
        CheckConstraint('quadro >= 0 AND quadro <= 7', name='check_aval_quadro'),
        CheckConstraint('velocidade_aula >= 0 AND velocidade_aula <= 7', name='check_aval_velocidade'),
        CheckConstraint('provas >= 0 AND provas <= 7', name='check_aval_provas'),
        CheckConstraint('trabalhos >= 0 AND trabalhos <= 7', name='check_aval_trabalhos'),
        CheckConstraint('projetos >= 0 AND projetos <= 7', name='check_aval_projetos'),
        CheckConstraint('interacao >= 0 AND interacao <= 7', name='check_aval_interacao'),
    )

class TipoPreferencia(Base):
   
    __tablename__ = 'tipos_preferencia'
    id_tipo = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False, unique=True)
    
    opcoes = relationship('OpcaoPreferencia', back_populates='tipo')

class OpcaoPreferencia(Base):
    __tablename__ = 'opcoes_preferencia'
    id_opcao = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False, unique=True)
    
    tipo_id = Column(Integer, ForeignKey('tipos_preferencia.id_tipo'), nullable=False)
    tipo = relationship('TipoPreferencia', back_populates='opcoes')
    
   
    coluna_mapeada = Column(String(50), nullable=False, unique=True)
    
    preferencias_alunos = relationship('PreferenciaAluno', back_populates='opcao')


class PerfilPreferencias(Base):
    __tablename__ = 'perfis_preferencias'
    
    id_perfil = Column(Integer, primary_key=True)
    
    aluno_id = Column(Integer, ForeignKey('alunos.id_aluno'), unique=True, nullable=False)
    aluno = relationship('Aluno', back_populates='perfil_preferencias')
    
    # O perfil é composto por uma lista de pesos
    preferencias = relationship('PreferenciaAluno', back_populates='perfil', cascade="all, delete-orphan")

class PreferenciaAluno(Base):
    __tablename__ = 'preferencias_aluno'
    
    id_preferencia = Column(Integer, primary_key=True)
    peso = Column(Integer, nullable=False, default=0)
    
    perfil_id = Column(Integer, ForeignKey('perfis_preferencias.id_perfil'), nullable=False)
    opcao_id = Column(Integer, ForeignKey('opcoes_preferencia.id_opcao'), nullable=False)
    
    perfil = relationship('PerfilPreferencias', back_populates='preferencias')
    opcao = relationship('OpcaoPreferencia', back_populates='preferencias_alunos')
    
    __table_args__ = (
        UniqueConstraint('perfil_id', 'opcao_id', name='uq_perfil_opcao'),
        CheckConstraint('peso >= 0 AND peso <= 7', name='check_peso'),
    )