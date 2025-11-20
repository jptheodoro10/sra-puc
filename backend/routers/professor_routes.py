from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
import crud

router = APIRouter(
    prefix="/prof",
    tags=["Professor"]
)

@router.get("/media/{prof_id}")
def get_media_professor(prof_id: int, db: Session = Depends(get_db)):
    """
    Retorna as médias calculadas do professor.
    """
    media = crud.get_media_professor(db, prof_id)

    if not media:
        raise HTTPException(status_code=404, detail="Professor não encontrado ou sem avaliações.")

    return {
        "professor_id": prof_id,
        "medias": {
            "slide": media.slide,
            "quadro": media.quadro,
            "velocidade_aula": media.velocidade_aula,
            "provas": media.provas,
            "trabalhos": media.trabalhos,
            "projetos": media.projetos,
            "interacao": media.interacao,
        }
    }
