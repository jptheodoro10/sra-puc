from sqlalchemy import Column, Integer, String, Float, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base  # Importa o Base do seu arquivo database.py

# --- TABELAS CENTRAIS: ALUNO, PROFESSOR, DISCIPLINA ---

class Aluno(Base):
    """
    Representa um Aluno no sistema.
    Um aluno pode ter um PerfilDePreferencias e fazer várias Avaliacoes.
    """
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
    """
    Representa um Professor.
    Um professor pode lecionar várias Turmas.
    """
    __tablename__ = 'professores'
    
    id_professor = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    
    # Relacionamento 1-para-N com Turma
    turmas = relationship('Turma', back_populates='professor')

class Curso(Base):
    """
    (Da sua imagem) Representa um curso/graduação.
    Ex: "Engenharia de Software", "Medicina".
    """
    __tablename__ = 'cursos'
    id_curso = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False, unique=True)
    
    disciplinas = relationship('Disciplina', back_populates='curso')

class Disciplina(Base):
    """
    Representa uma Disciplina ou Matéria (ex: "Banco de Dados").
    Uma disciplina pertence a um Curso e pode ter várias Turmas.
    """
    __tablename__ = 'disciplinas'
    
    id_disciplina = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False, unique=True)
    curso_id = Column(Integer, ForeignKey('cursos.id_curso'), nullable=True) # Opcional
    
    curso = relationship('Curso', back_populates='disciplinas')
    turmas = relationship('Turma', back_populates='disciplina')

class Turma(Base):
    """
    Representa uma instância de uma Disciplina, lecionada por um Professor
    em um semestre específico.
    (Ex: Disciplina "Banco de Dados", Turma "3WA", Semestre "2025.1")
    """
    __tablename__ = 'turmas'
    
    id_turma = Column(Integer, primary_key=True)
    nome_turma = Column(String(50), nullable=False) # ex: "3WA", "3WB"
    semestre = Column(String(20), nullable=False) # ex: "2025.1"
    
    professor_id = Column(Integer, ForeignKey('professores.id_professor'), nullable=False)
    disciplina_id = Column(Integer, ForeignKey('disciplinas.id_disciplina'), nullable=False)
    
    professor = relationship('Professor', back_populates='turmas')
    disciplina = relationship('Disciplina', back_populates='turmas')
    
    avaliacoes = relationship('Avaliacao', back_populates='turma')

# --- SISTEMA DE AVALIAÇÃO (COLUNAS FIXAS) ---

class Avaliacao(Base):
    """
    Armazena a avaliação de um Aluno para uma Turma específica.
    Contém as notas (0-7) para cada critério (colunas fixas).
    O backend usará (AVG) desses dados para criar o "perfil do professor".
    """
    __tablename__ = 'avaliacoes'
    
    id_avaliacao = Column(Integer, primary_key=True)
    semestre = Column(String(20), nullable=False) # Snapshot do semestre da avaliação
    
    turma_id = Column(Integer, ForeignKey('turmas.id_turma'), nullable=False)
    aluno_id = Column(Integer, ForeignKey('alunos.id_aluno'), nullable=False)
    
    turma = relationship('Turma', back_populates='avaliacoes')
    aluno = relationship('Aluno', back_populates='avaliacoes')
    
    # Critérios fixos avaliados (0-7)
    # O backend irá mapear as OpcaoPreferencia para estas colunas
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

# --- SISTEMA DE PREFERÊNCIAS (DINÂMICO, DA IMAGEM) ---

class TipoPreferencia(Base):
    """
    (Da imagem) A "categoria" da preferência.
    Ex: "Forma de Lecionar", "Método Avaliativo"
    """
    __tablename__ = 'tipos_preferencia'
    id_tipo = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False, unique=True)
    
    opcoes = relationship('OpcaoPreferencia', back_populates='tipo')

class OpcaoPreferencia(Base):
    """
    (Da imagem) O critério específico que o aluno pode ponderar.
    Ex: "Usa Slides", "Usa Quadro", "Provas difíceis"
    """
    __tablename__ = 'opcoes_preferencia'
    id_opcao = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False, unique=True)
    
    tipo_id = Column(Integer, ForeignKey('tipos_preferencia.id_tipo'), nullable=False)
    tipo = relationship('TipoPreferencia', back_populates='opcoes')
    
    # A "MÁGICA": Como mapear esta opção (ex: "Usa Slides")
    # para a coluna da tabela 'Avaliacao' (ex: "slide")
    coluna_mapeada = Column(String(50), nullable=False, unique=True)
    
    preferencias_alunos = relationship('PreferenciaAluno', back_populates='opcao')


class PerfilPreferencias(Base):
    """
    (Da imagem) O "cabeçalho" do perfil de um aluno.
    Liga um Aluno a um conjunto de pesos (PreferenciaAluno).
    """
    __tablename__ = 'perfis_preferencias'
    
    id_perfil = Column(Integer, primary_key=True)
    
    aluno_id = Column(Integer, ForeignKey('alunos.id_aluno'), unique=True, nullable=False)
    aluno = relationship('Aluno', back_populates='perfil_preferencias')
    
    # O perfil é composto por uma lista de pesos
    preferencias = relationship('PreferenciaAluno', back_populates='perfil', cascade="all, delete-orphan")

class PreferenciaAluno(Base):
    """
    (Da imagem) A tabela de junção que armazena o PESO (0-7)
    que um Aluno (via Perfil) dá para uma OpcaoPreferencia.
    """
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