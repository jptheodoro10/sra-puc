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


# --- FUNÇÃO NOVA ---
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
        # db.commit() # Depende se você quer commitar aqui ou no final
        db.flush() # 'flush' atribui o ID sem commitar
    else:
        perfil_db = aluno.perfil_preferencias
        # Limpa as preferências antigas para recriá-las
        db.query(models.PreferenciaAluno)\
          .filter_by(perfil_id=perfil_db.id_perfil).delete()

    # 2. O VETOR "TRADUZIDO" (A Lógica de Negócio)
    # Este dicionário conterá o vetor final (ex: {'slide': 1, 'quadro': 7, ...})
    vetor_final = {}

    # --- REGRA DE TRADUÇÃO 1: Metodologia (formaLecionar) ---
    # Hipótese: 'Teórica' = slide, 'Prática' = quadro, 'Mista' = ambos
    peso_metodologia = perfil_data.formaLecionarImportancia
    if perfil_data.formaLecionar == "Teórica":
        vetor_final['slide'] = peso_metodologia
        vetor_final['quadro'] = 1 # Valor mínimo
    elif perfil_data.formaLecionar == "Prática":
        vetor_final['slide'] = 1 # Valor mínimo
        vetor_final['quadro'] = peso_metodologia
    elif perfil_data.formaLecionar == "Mista":
        vetor_final['slide'] = peso_metodologia
        vetor_final['quadro'] = peso_metodologia

    # --- REGRA DE TRADUÇÃO 2: Avaliação (formaAvaliar) ---
    # Hipótese: O valor selecionado recebe o peso, os outros recebem 1
    peso_avaliacao = perfil_data.formaAvaliarImportancia
    vetor_final['provas'] = 1
    vetor_final['trabalhos'] = 1
    vetor_final['projetos'] = 1
    
    if perfil_data.formaAvaliar == "Provas":
        vetor_final['provas'] = peso_avaliacao
    elif perfil_data.formaAvaliar == "Trabalhos":
        vetor_final['trabalhos'] = peso_avaliacao
    elif perfil_data.formaAvaliar == "Projetos":
        vetor_final['projetos'] = peso_avaliacao
        
    # --- REGRA DE TRADUÇÃO 3: Ritmo (ritmoAula) ---
    # Hipótese: Ignoramos 'Lento/Rápido' e usamos a 'Importancia' como o peso
    # para a 'velocidade_aula'.
    vetor_final['velocidade_aula'] = perfil_data.ritmoAulaImportancia
    
    # --- REGRA DE TRADUÇÃO 4: Incentivo (incentivo) ---
    # Hipótese: Usamos a 'Importancia' como o peso para 'interacao'.
    vetor_final['interacao'] = perfil_data.incentivoImportancia

    # 3. SALVAR O VETOR NO BANCO
    # Agora, converte o `vetor_final` em linhas `PreferenciaAluno`
    
    preferencias_para_salvar = []
    for coluna, peso in vetor_final.items():
        if coluna in opcoes_map: # Garante que a coluna existe
            preferencias_para_salvar.append(
                models.PreferenciaAluno(
                    perfil_id=perfil_db.id_perfil,
                    opcao_id=opcoes_map[coluna],
                    peso=peso
                )
            )

    if preferencias_para_salvar:
        db.add_all(preferencias_para_salvar)
    
    db.commit()
    db.refresh(perfil_db) # Recarrega o perfil com as novas preferências
    return perfil_db


# --- FUNÇÕES NOVAS (Para Rota de Recomendação) ---

# Esta lista define o "espaço vetorial" da comparação
# Deve ser idêntica à da sua rota de recomendação
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

def get_all_professores_avg_ratings(db: Session):
    """
    Calcula a média de avaliação de TODOS os professores em todas as
    categorias (features) e retorna uma lista de resultados.
    Essencial para construir os "vetores dos professores".
    """
    
    # Cria dinamicamente as colunas de média (ex: AVG(slide) AS avg_slide)
    avg_cols = [
        func.avg(getattr(models.Avaliacao, col)).label(f"avg_{col}")
        for col in FEATURE_NAMES
    ]
    
    # Executa a query que junta Professor -> Turma -> Avaliacao
    # e agrupa por professor para calcular as médias.
    return db.query(
        models.Professor.id_professor,
        models.Professor.nome,
        *avg_cols # Desempacota as colunas (AVG(slide), AVG(quadro), ...)
    ).join(
        models.Turma, models.Professor.id_professor == models.Turma.professor_id
    ).join(
        models.Avaliacao, models.Turma.id_turma == models.Avaliacao.turma_id
    ).group_by(
        models.Professor.id_professor, models.Professor.nome
    ).all()