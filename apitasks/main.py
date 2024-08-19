from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Configuração do banco de dados SQLite
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Definição do modelo Task
class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    task = Column(String, index=True)

# Criar o banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Função para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Populando o banco de dados com dados iniciais
def populate_db():
    db = SessionLocal()
    if db.query(Task).count() == 0:  # Verifica se o banco de dados está vazio
        tasks = ["Small task", "A much bigger task description", "Another task", "Short", "Extremely long and detailed task description", "Small task again"]
        for task in tasks:
            db.add(Task(task=task))
        db.commit()
    db.close()

populate_db()

# Rota para listar todas as tasks
@app.get("/tasks/")
def read_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return [{"id": task.id, "task": task.task} for task in tasks]
