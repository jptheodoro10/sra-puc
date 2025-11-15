from fastapi import FastAPI
from routers import auth as auth_router
from routers import aluno as aluno_router

app = FastAPI()

app.include_router(auth_router.router)
app.include_router(aluno_router.router)
