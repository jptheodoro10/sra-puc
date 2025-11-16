from fastapi import APIRouter, Depends, HTTPException, status
import auth #onde esta a get_current_aluno()
import schemas
import crud
import models
from sqlalchemy.orm import Session
from database import get_db
import numpy as np

router= APIRouter(
    prefix="/aluno", 
    tags=["Aluno"],
    dependencies=[Depends(auth.get_current_aluno)] 
)




# Esta lista DEVE ser idêntica à do crud.py
FEATURE_NAMES = [
    'slide', 'quadro', 'velocidade_aula', 
    'provas', 'trabalhos', 'projetos', 'interacao'
]

def calculate_cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    """Calcula a similaridade de cossenos entre dois vetores."""
    dot_product = np.dot(vec_a, vec_b)
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    
    # Evita divisão por zero se um vetor for nulo (sem preferências/avaliações)
    if norm_a == 0 or norm_b == 0:
        return 0.0
        
    return dot_product / (norm_a * norm_b)

# todas as rotas abaixo estão protegidas, nao precisa de Depends(get_current aluno) pois colocamos no router

#rota que salva o perfil:

@router.post("/me/perfil", response_model=schemas.PerfilPreferencias)
def salvar_perfil_aluno(
    perfil_data: schemas.PerfilFrontend, # Recebe o schema do frontend
    db: Session = Depends(get_db),
    current_aluno: models.Aluno = Depends(auth.get_current_aluno)
):
    """
    recebe os dados do formulario e transforma em forma de vetor
    """
    
    # 1. Pega o mapa de 'coluna' -> 'id_opcao' (ex: 'slide' -> 1)
    opcoes_map = crud.get_opcoes_dict(db)
    if not opcoes_map:
        raise HTTPException(
            status_code=500, 
            detail="Banco de dados não populado com OpcoesPreferencia."
        )

    
    try:
        perfil_salvo = crud.create_or_update_aluno_perfil(
            db=db, 
            aluno=current_aluno, 
            perfil_data=perfil_data, 
            opcoes_map=opcoes_map
        )
        return perfil_salvo
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao salvar perfil: {e}"
        )
    
    
@router.get("/recomendacoes", response_model=list[schemas.ProfessorComSimilaridade])
def get_recomendacoes(
    db: Session = Depends(get_db),
    current_aluno: schemas.Aluno = Depends(auth.get_current_aluno)
):
    """
    Calcula e retorna uma lista de professores ranqueados 
    por similaridade de cossenos com as preferências do aluno logado.
    """
    
    # --- 1. OBTER O VETOR DO ALUNO (VETOR A) ---
    
    perfil = crud.get_perfil_completo_by_aluno_id(db, aluno_id=current_aluno.id_aluno)
    
    if not perfil or not perfil.preferencias:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Perfil de preferências não encontrado. Por favor, preencha suas preferências primeiro."
        )

    # Converte as preferências do banco em um dicionário
    # (Ex: {'slide': 7, 'quadro': 2, 'provas': 5, ...})
    preferencias_dict = {
        pref.opcao.coluna_mapeada: pref.peso 
        for pref in perfil.preferencias
    }
    
    # Converte o dicionário em um vetor numpy na ORDEM CORRETA
    # (Ex: [7, 2, 0, 5, 0, 0, 0])
    aluno_vector = np.array([
        preferencias_dict.get(feature, 0) for feature in FEATURE_NAMES
    ])

    # --- 2. OBTER OS VETORES DOS PROFESSORES (VETORES B) ---
    
    # Busca as médias de todos os professores
    prof_ratings_list = crud.get_all_professores_avg_ratings(db)
    
    if not prof_ratings_list:
        return [] # Retorna lista vazia se nenhum professor foi avaliado

    resultados = []
    
    # --- 3. CALCULAR A SIMILARIDADE ---

    for prof_data in prof_ratings_list:
        # prof_data é um objeto com (id_professor, nome, avg_slide, avg_quadro, ...)
        
        # Converte as médias do professor em um vetor numpy na MESMA ORDEM
        prof_vector = np.array([
            getattr(prof_data, f"avg_{feature}", 0) for feature in FEATURE_NAMES
        ])
        
        # Calcula a similaridade
        similaridade = calculate_cosine_similarity(aluno_vector, prof_vector)
        
        resultados.append({
            "id_professor": prof_data.id_professor,
            "nome": prof_data.nome,
            "similaridade": similaridade
        })

    # --- 4. RANQUEAR E RETORNAR ---
    
    # Ordena a lista pela similaridade, da maior para a menor
    resultados_ordenados = sorted(
        resultados, 
        key=lambda x: x['similaridade'], 
        reverse=True
    )
    
    return resultados_ordenados