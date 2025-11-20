from sqlalchemy.orm import Session, joinedload
import models
import schemas
from sqlalchemy import func


def get_aluno_by_id(db: Session, aluno_id: int):
   
    return db.query(models.Aluno).filter(models.Aluno.id_aluno == aluno_id).first()

def get_aluno_by_matricula(db: Session, matricula: str):
    #usada no login
    return db.query(models.Aluno).filter(models.Aluno.matricula == matricula).first()

#Funções das próximas rotas:

# def get_disciplinas(db: Session): ...
# def get_opcoes_preferencia(db: Session): ...
# def get_professor_profile_vector(db: Session, professor_id: int, disciplina_id: int): ...
# def get_aluno_preference_vector(db: Session, aluno_id: int): ...
def get_opcoes_dict(db: Session) -> dict[str, int]:
    """
    Busca todas as OpcaoPreferencia e retorna um dicionário
    mapeando a 'coluna_mapeada' para o 'id_opcao'.
    
    Ex: {'slide': 1, 'quadro': 2, 'provas': 3, ...}
    """
    opcoes = db.query(models.OpcaoPreferencia).all()
    return {op.coluna_mapeada: op.id_opcao for op in opcoes}



def create_or_update_aluno_perfil(
    db: Session, 
    aluno: models.Aluno, 
    perfil_data: schemas.PerfilFrontend, 
    opcoes_map: dict[str, int]
):
    """
    Recebe os dados do formulário (PerfilFrontend), 'traduz'
    para o vetor de features e salva no banco de dados.
    """
    
    # 1. Garante que o Aluno tenha um PerfilPreferencias
    if not aluno.perfil_preferencias:
        perfil_db = models.PerfilPreferencias(aluno=aluno)
        db.add(perfil_db)
     
        db.flush() # atribui o ID sem commitar
    else:
        perfil_db = aluno.perfil_preferencias
        # limpa as preferências antigas para recriá-las
        db.query(models.PreferenciaAluno)\
          .filter_by(perfil_id=perfil_db.id_perfil).delete()

    # 2. O VETOR "TRADUZIDO" 
    # Este dicionário conterá o vetor final (ex: {'slide': 1, 'quadro': 7, ...})
    vetor_final = {}

    #  Metodologia (formaLecionar) 

    imp = perfil_data.formaLecionarImportancia

    vetor_final["slide"] = 0
    vetor_final["quadro"] = 0

    if perfil_data.formaLecionar == "Teórica":
        vetor_final["slide"] = imp
    elif perfil_data.formaLecionar == "Prática":
        vetor_final["quadro"] = imp

    # =============== 2. Forma de avaliação ==========================
    imp = perfil_data.formaAvaliarImportancia

    vetor_final["provas"] = 0
    vetor_final["trabalhos"] = 0
    vetor_final["projetos"] = 0

    if perfil_data.formaAvaliar == "Provas":
        vetor_final["provas"] = imp
    elif perfil_data.formaAvaliar == "Trabalhos":
        vetor_final["trabalhos"] = imp
    elif perfil_data.formaAvaliar == "Projetos":
        vetor_final["projetos"] = imp

    # 3. Ritmo da Aula 
    imp = perfil_data.ritmoAulaImportancia

    vetor_final["velocidade_aula"] = imp 
    #  4. Partipacao em aula 
    imp = perfil_data.incentivoImportancia

    vetor_final["interacao"] = imp
    # 3. SALVAR NO BANCO
    preferencias = []
    for nome, peso in vetor_final.items():
        if nome in opcoes_map:
            preferencias.append(
                models.PreferenciaAluno(
                    perfil_id=perfil_db.id_perfil,
                    opcao_id=opcoes_map[nome],
                    peso=peso
                )
            )

    if preferencias:
        db.add_all(preferencias)

    db.commit()
    db.refresh(perfil_db)

    return perfil_db



# Esta lista define o "espaço vetorial" da comparação
FEATURE_NAMES = [
    'slide', 'quadro', 'velocidade_aula',
    'provas', 'trabalhos', 'projetos', 'interacao'
]

def get_perfil_completo_by_aluno_id(db: Session, aluno_id: int):
    """
    Busca o perfil do aluno e já carrega (eager load)
    as preferências e as opções associadas.
    Essencial para construir o "vetor do aluno".
    """
    return db.query(models.PerfilPreferencias)\
             .filter(models.PerfilPreferencias.aluno_id == aluno_id)\
             .options(
                 joinedload(models.PerfilPreferencias.preferencias)\
                 .joinedload(models.PreferenciaAluno.opcao)
             ).first()

def get_disciplinas(db: Session):
    """Retorna todas as disciplinas cadastradas."""
    return db.query(models.Disciplina).all()


def get_professores_avg_ratings_by_disciplina(db: Session, disciplina_id: int):
    avg_cols = [
        func.avg(getattr(models.Avaliacao, col)).label(f"avg_{col}")
        for col in FEATURE_NAMES
    ]
    
    return db.query(
        models.Professor.id_professor,
        models.Professor.nome,
        *avg_cols 
    ).join(
        models.Turma, models.Professor.id_professor == models.Turma.professor_id
    ).join(
        models.Avaliacao, models.Turma.id_turma == models.Avaliacao.turma_id
    ).filter( # --- FILTRO ADICIONADO ---
        models.Turma.disciplina_id == disciplina_id
    ).group_by(
        models.Professor.id_professor, models.Professor.nome
    ).all()

# ----------------------------------

def get_media_professor(db: Session, prof_id: int):
    result = db.query(
        func.avg(models.AvaliacaoProfessor.slide).label("slide"),
        func.avg(models.AvaliacaoProfessor.quadro).label("quadro"),
        func.avg(models.AvaliacaoProfessor.velocidade_aula).label("velocidade_aula"),
        func.avg(models.AvaliacaoProfessor.provas).label("provas"),
        func.avg(models.AvaliacaoProfessor.trabalhos).label("trabalhos"),
        func.avg(models.AvaliacaoProfessor.projetos).label("projetos"),
        func.avg(models.AvaliacaoProfessor.interacao).label("interacao"),
    ).filter(
        models.AvaliacaoProfessor.id_professor == prof_id
    ).first()

    return result