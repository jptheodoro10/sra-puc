from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
import models 
import auth   

def seed_data(db: Session):
    
    #  verificar se metadados ja existem:
    if db.query(models.TipoPreferencia).first() is not None:
        print("Metadados (Tipos/Opções) já existem. Pulando o seeding.")
    else:
        print("Populando Tipos e Opções de Preferência...")
        
        # popular metdados:
        tipo_ensino = models.TipoPreferencia(nome="Forma de Lecionar")
        tipo_avaliacao = models.TipoPreferencia(nome="Método Avaliativo")
        tipo_ritmo = models.TipoPreferencia(nome="Ritmo da Aula")
        tipo_engajamento = models.TipoPreferencia(nome="Engajamento")
        db.add_all([tipo_ensino, tipo_avaliacao, tipo_ritmo, tipo_engajamento])
        
        op_slide = models.OpcaoPreferencia(tipo=tipo_ensino, nome="Usa Slides", coluna_mapeada="slide")
        op_quadro = models.OpcaoPreferencia(tipo=tipo_ensino, nome="Usa Quadro", coluna_mapeada="quadro")
        op_provas = models.OpcaoPreferencia(tipo=tipo_avaliacao, nome="Foco em Provas", coluna_mapeada="provas")
        op_trabalhos = models.OpcaoPreferencia(tipo=tipo_avaliacao, nome="Foco em Trabalhos", coluna_mapeada="trabalhos")
        op_projetos = models.OpcaoPreferencia(tipo=tipo_avaliacao, nome="Foco em Projetos", coluna_mapeada="projetos")
        op_velocidade = models.OpcaoPreferencia(tipo=tipo_ritmo, nome="Ritmo da Aula", coluna_mapeada="velocidade_aula")
        op_interacao = models.OpcaoPreferencia(tipo=tipo_engajamento, nome="Interação e Participação", coluna_mapeada="interacao")
        db.add_all([op_slide, op_quadro, op_provas, op_trabalhos, op_projetos, op_velocidade, op_interacao])
        db.commit()
        print("Metadados populados.")
        
    # dados de simulacao:
    if db.query(models.Aluno).first() is not None:
        print("Dados de simulação (Alunos/Professores) já existem. Pulando.")
    else:
        print("Populando dados de simulação (Alunos, Professores, Avaliações)...")
        
        curso_es = models.Curso(nome="Engenharia de Software")
        disc_bd = models.Disciplina(nome="Banco de Dados", curso=curso_es)
        prof_adriano = models.Professor(nome="Prof. Adriano")
        prof_carla = models.Professor(nome="Prof. Carla")
        turma_adriano = models.Turma(nome_turma="3WA", semestre="2025.1", professor=prof_adriano, disciplina=disc_bd)
        turma_carla = models.Turma(nome_turma="3WB", semestre="2025.1", professor=prof_carla, disciplina=disc_bd)
        
        
        # criar hash de senha para simulação (ex: "puc123")
        sim_password_hash = auth.get_password_hash("puc123")

        # alunos (todos com a senha simulada 'hashaeada')
        aluno_joao = models.Aluno(
            nome="João Silva", 
            matricula="2110001",                   
            hashed_password=sim_password_hash      
        )
        aluno_maria = models.Aluno(
            nome="Maria Souza", 
            matricula="2110002",                 
            hashed_password=sim_password_hash      
        )
        aluno_pedro = models.Aluno(
            nome="Pedro Costa", 
            matricula="2110003",                   
            hashed_password=sim_password_hash      
        )

        aluno_Veeck = models.Aluno(
            nome = "Felipe Veeck",
            matricula= "2110004",
            hashed_password = sim_password_hash
        )
        
        aluno_Python = models.Aluno(
            nome = "Vitor Python",
            matricula= "2110005",
            hashed_password = sim_password_hash
        )
        
        # avaliações simuladas
        aval1_adriano = models.Avaliacao(aluno=aluno_maria, turma=turma_adriano, semestre="2025.1", slide=7, quadro=2, velocidade_aula=6, provas=4, trabalhos=5, projetos=5, interacao=5)
        aval2_adriano = models.Avaliacao(aluno=aluno_pedro, turma=turma_adriano, semestre="2025.1", slide=6, quadro=3, velocidade_aula=7, provas=5, trabalhos=5, projetos=5, interacao=6)
        aval1_carla = models.Avaliacao(aluno=aluno_maria, turma=turma_carla, semestre="2025.1", slide=2, quadro=7, velocidade_aula=4, provas=6, trabalhos=5, projetos=5, interacao=7)
        aval2_carla = models.Avaliacao(aluno=aluno_pedro, turma=turma_carla, semestre="2025.1", slide=3, quadro=6, velocidade_aula=5, provas=6, trabalhos=5, projetos=5, interacao=6)
        
        db.add_all([
            curso_es, disc_bd, prof_adriano, prof_carla, turma_adriano, turma_carla,
            aluno_joao, aluno_maria, aluno_pedro, aluno_Veeck, aluno_Python,
            aval1_adriano, aval2_adriano, aval1_carla, aval2_carla
        ])
        
        db.commit()
        print("Dados de simulação populados.")


def init_database():
    print("Iniciando a criação do banco de dados...")
    # limpa o banco 
    Base.metadata.drop_all(bind=engine) 
    
    # cria todas as tabelas 
    try:
        Base.metadata.create_all(bind=engine)
        print("Tabelas criadas com sucesso.")
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")
        return

    # popula os dados
    db = SessionLocal()
    try:
        seed_data(db)
    except Exception as e:
        print(f"Erro ao popular dados (seeding): {e}")
        db.rollback() 
    finally:
        db.close()
        print("Conexão com o banco fechada.")

if __name__ == "__main__":
    init_database()