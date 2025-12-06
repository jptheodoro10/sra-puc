# SRA PUC-Rio

## Visão Geral
Muitos alunos enfrentam dificuldades ao escolher professores para as disciplinas do semestre: decisões baseadas em avaliações subjetivas, experiências isoladas ou falta de informação consolidada. O SRA-PUC (Sistema de Recomendação Acadêmica) nasce para resolver esse problema.
O objetivo do sistema é recomendar professores alinhados ao perfil e às preferências do aluno, utilizando dados reais de avaliações acadêmicas. A aplicação combina usabilidade, modelagem de dados e algoritmos de recomendação para entregar uma experiência personalizada e transparente.

## Como funciona
O SRA-PUC coleta preferências do aluno (forma de lecionar, método avaliativo, ritmo, engajamento, etc.) e compara essas informações com o histórico de avaliações dos professores.
O algoritmo usa **distância euclidiana ponderada**, permitindo quantificar, de forma objetiva, o quão próximo cada professor está do perfil desejado.
Em resumo:
O aluno informa suas preferências.
O backend processa essas informações, consulta o banco e aplica o algoritmo.
A interface exibe uma lista ordenada de professores recomendados, do mais compatível ao menos compatível.

## Como funciona internamente (NumPy e vetores)
Internamente, o SRA-PUC representa as preferências do aluno e os atributos dos professores como vetores NumPy. Cada característica (como uso de slides, método avaliativo ou ritmo da aula) é mapeada para uma posição fixa no vetor.
<br>O algoritmo funciona assim:
- As preferências do aluno são convertidas em um vetor NumPy.
- Cada professor possui seu próprio vetor no mesmo formato, formado pelas avaliacoes feitas sobre ele.
- Calculamos a distância euclidiana ponderada entre os vetores.
- Professores cuja distância é menor são considerados mais compatíveis.
- <br>O uso de NumPy torna o cálculo rápido, consistente e fácil de expandir para novas features.

## Arquitetura da Solução
A aplicação é full-stack e foi desenvolvida com:
- **Frontend em React/Vite**, focado em simplicidade e responsividade
- **Backend em FastAPI (Python)**, responsável por autenticação, CRUDs e recomendação
- **PostgreSQL** hospedado no Neon, **integrado via SQLAlchemy**
- **Autenticação JWT**
- **Algoritmo de recomendação próprio**

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
