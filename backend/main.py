from fastapi import FastAPI
from routers import auth_router as auth_router
from routers import aluno_routes as aluno_router
from routers import professor_routes as prof_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(auth_router.router)
app.include_router(aluno_router.router)

origins = [
    "http://localhost:5173",  # Vite
    "http://localhost:3000",  # React 
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],   
    allow_headers=["*"],   
)
