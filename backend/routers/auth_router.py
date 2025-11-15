from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
import schemas
import auth
import crud

router = APIRouter(tags=["auth"])


@router.post("/login", response_model=schemas.Token)
def login(request: schemas.LoginRequest, db: Session = Depends(get_db)):
    aluno = auth.authenticate_user(db, request.matricula, request.senha)

    if not aluno:
        raise HTTPException(status_code=400, detail="Matrícula ou senha incorretos")

    token = auth.create_access_token(
        data={"sub": aluno.matricula, "aluno_id": aluno.id_aluno},
    )

    return {"access_token": token, "token_type": "bearer"}
