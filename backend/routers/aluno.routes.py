from fastapi import APIRouter, Depends
import auth #onde esta a get_current_aluno()

router_privado_aluno = APIRouter(
    prefix="/aluno", 
    tags=["Aluno"],
    dependencies=[Depends(auth.get_current_aluno)] 
)

# todas as rotas abaixo estão protegidas, nao precisa de Depends(get_current aluno) pois colocamos no router

