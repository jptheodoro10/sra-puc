# SRA PUC-Rio

Projeto do Sistema de Recomendacao Academica para a PUC-RIO. Aplicação full-stack (FastAPI + React/Vite). Use bancos separados por ambiente!

## Requisitos

- Python 3.11+
- Node.js 18+
- Postgres local

## Backend (FastAPI)

1. Instale : `pip install -r requirements.txt` (dentro de `backend/`).
2. Copie `backend/.env.example` para `backend/.env` e preencha:
   - `DATABASE_URL=postgresql://user:pass@localhost:5432/sra_dev` (use seu Postgres local)
   - `SECRET_KEY=` string longa e aleatória (JWT), pode gerar com `openssl rand -hex 32`
   - `ACCESS_TOKEN_EXPIRE_MINUTES=` opcional (padrão 1440 = 24h)
3. Rode: `uvicorn main:app --reload` (em `backend/`).

## Frontend (React/Vite)

1. Em `frontend/`: `npm install`.
2. Copie `frontend/.env.example` para `frontend/.env` e ajuste:
   - `VITE_API_URL=http://localhost:8000` (URL do frontend)
3. Rode: `npm run dev`.

## Usuário de teste (para login)

Com o backend configurado (env apontando para seu banco), crie um usuário padrão:

```cd backend
python3 - <<`PY`
from database import SessionLocal
from auth import get_password_hash
import models
db = SessionLocal()
matricula = "teste123"; senha = "123456"
existing = db.query(models.Aluno).filter(models.Aluno.matricula == matricula).first()
if existing:
    print(f"Aluno já existe: id={existing.id_aluno}, matricula={existing.matricula}")
else:
    aluno = models.Aluno(matricula=matricula, nome="Usuário Teste", hashed_password=get_password_hash(senha))
    db.add(aluno); db.commit(); db.refresh(aluno)
    print(f"Criado aluno id={aluno.id_aluno}")
db.close()
PY
```

matricula `teste123`
senha `123456`.

## Banco de dados: local vs Neon

- Padrão para quem clonar: Postgres local (`DATABASE_URL=postgresql://user:pass@localhost:5432/sra_dev`).
- Se quiser usar Neon (ou outro Postgres hospedado):
  1. Crie a instância no provedor e copie a connection string.
  2. Ajuste `DATABASE_URL` no seu `.env` para essa string (inclua `sslmode` se exigido).

## Variáveis de ambiente (resumo)

- Backend: `DATABASE_URL`, `SECRET_KEY`, `ACCESS_TOKEN_EXPIRE_MINUTES` (opcional).
- Frontend: `VITE_API_URL` (URL da API).
