from fastapi import APIRouter, Depends, HTTPException, status
import auth #onde esta a get_current_aluno()
import schemas
import crud
import models
from sqlalchemy.orm import Session
from database import get_db
import numpy as np
import math
from constants.features import FEATURE_NAMES


router= APIRouter(
    prefix="/aluno", 
    tags=["Aluno"],
    dependencies=[Depends(auth.get_current_aluno)] 
)



# todas as rotas abaixo estão protegidas, nao precisa de Depends(get_current aluno) pois colocamos no router

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


@router.get("/disciplinas", response_model=list[schemas.Disciplina])
def get_all_disciplinas(db: Session = Depends(get_db)):
    return crud.get_disciplinas(db)
    
    
@router.get("/recomendacoes", response_model=list[schemas.ProfessorComSimilaridade])
def get_recomendacoes(
    disciplina_id: int,
    db: Session = Depends(get_db),
    current_aluno: models.Aluno = Depends(auth.get_current_aluno)
):
    """
    Calcula e retorna professores ranqueados por similaridade
    filtrados pela disciplina fornecida.
    Também retorna a quantidade de estrelas (0 a 5).
    """

    # 1. Perfil do aluno
    perfil = crud.get_perfil_completo_by_aluno_id(db, aluno_id=current_aluno.id_aluno)

    if not perfil or not perfil.preferencias:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil de preferências não encontrado. Preencha suas preferências primeiro."
        )

    preferencias_dict = {
        pref.opcao.coluna_mapeada: pref.peso
        for pref in perfil.preferencias
    }

    aluno_vector = np.array([
        preferencias_dict.get(feature, 0)
        for feature in FEATURE_NAMES
    ])

    pesos_vector = aluno_vector.copy()

    # 2. Médias dos professores
    prof_ratings_list = crud.get_professores_avg_ratings_by_disciplina(
        db, disciplina_id=disciplina_id
    )

    if not prof_ratings_list:
        return []

    resultados = []

    # 3. Similaridade + estrelas
    for prof_data in prof_ratings_list:

        prof_vector = np.array([
            float(getattr(prof_data, f"avg_{feature}", 0) or 0)
            for feature in FEATURE_NAMES
        ])

        similaridade = weighted_euclidean_similarity(
            aluno_vector,
            prof_vector,
            pesos_vector
        )

        # conversão similaridade (0 a 1) → estrelas (0 a 5)
        estrelas = similaridade * 5

        resultados.append({
            "id_professor": prof_data.id_professor,
            "nome": prof_data.nome,
            "similaridade": similaridade,
            "estrelas": estrelas
        })

    # 4. Ordenar
    resultados_ordenados = sorted(
        resultados,
        key=lambda p: p["similaridade"],
        reverse=True
    )
    for r in resultados_ordenados:
        print(r["nome"], 
          "sim:", round(r["similaridade"], 3), 
          "estrelas:", round(r["estrelas"], 2))


    return resultados_ordenados


def weighted_euclidean_similarity(aluno_vector, prof_vector, pesos_vector):
    """
    Calcula similaridade baseada na distância euclidiana ponderada,
    normalizando pela maior distância possível (escala 0-7).
    """
    diff = aluno_vector - prof_vector
    weighted = pesos_vector * (diff ** 2)
    dist = float(np.sqrt(weighted.sum()))

    # Máxima distância considerando notas/avaliações entre 0 e 7.
    max_dist = float(np.sqrt((pesos_vector * (7 ** 2)).sum()))
    if max_dist == 0:
        return 0.0

    ratio =  dist / max_dist
    similarity = 1 / (1 + math.exp(10 * (ratio - 0.5)))

 
    return similarity
