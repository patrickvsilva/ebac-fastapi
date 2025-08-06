# Configurando o banco de dados SQLite
import os
import secrets

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from sqlalchemy import Boolean, Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", None)
USER = os.getenv("USER", None)
PASSWORD = os.getenv("PASSWORD", None)
if DATABASE_URL is None or USER is None or PASSWORD is None:
    raise ValueError(
        "As variáveis de ambiente DATABASE_URL, USER e PASSWORD não estão definidas."
    )
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


class TarefaDB(Base):
    __tablename__ = "tarefas"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True)
    descricao = Column(String, index=True)
    concluida = Column(Boolean, default=False)


Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()

security = HTTPBasic()


def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    is_user_correct = secrets.compare_digest(credentials.username, USER)
    is_password_correct = secrets.compare_digest(credentials.password, PASSWORD)
    if not is_user_correct:
        raise HTTPException(
            status_code=401,
            detail="Usuário inválido",
            headers={"WWW-Authenticate": "Basic"},
        )

    if not is_password_correct:
        raise HTTPException(
            status_code=401,
            detail="Senha inválida",
            headers={"WWW-Authenticate": "Basic"},
        )

    if not is_user_correct or not is_password_correct:
        raise HTTPException(
            status_code=401,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Basic"},
        )


class Tarefa(BaseModel):
    nome: str
    descricao: str
    concluida: bool = False


@app.post("/adicionar_tarefa")
def read_root(
    tarefa: Tarefa,
    db: SessionLocal = Depends(get_db),
    credentials: HTTPBasicCredentials = Depends(authenticate),
):
    tarefa_db = (
        db.query(TarefaDB)
        .filter(TarefaDB.nome == tarefa.nome, TarefaDB.descricao == tarefa.descricao)
        .first()
    )

    if tarefa_db:
        raise HTTPException(status_code=400, detail=f"Tarefa {tarefa.nome} já existe")
    nova_tarefa = TarefaDB(
        nome=tarefa.nome, descricao=tarefa.descricao, concluida=tarefa.concluida
    )
    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)

    return {"message": f"Tarefa {tarefa.nome} adicionada com sucesso!"}


@app.get("/listar_tarefas")
def listar_tarefas(
    page: int = 1,
    size: int = 10,
    order_by: str = "",
    db: SessionLocal = Depends(get_db),
    credentials: HTTPBasicCredentials = Depends(authenticate),
):
    if page < 1 or size < 1:
        raise HTTPException(status_code=400, detail="Parâmetros de paginação inválidos")
    if order_by not in ["", "nome", "descricao", "concluida"]:
        raise HTTPException(status_code=400, detail="Parâmetro 'order_by' inválido")
    start = (page - 1) * size

    if order_by == "":
        tarefas = db.query(TarefaDB).offset(start).limit(size).all()
    else:
        tarefas = (
            db.query(TarefaDB)
            .order_by(getattr(TarefaDB, order_by))
            .offset(start)
            .limit(size)
            .all()
        )
    tarefas_pagina = [
        {
            "nome": tarefa.nome,
            "descricao": tarefa.descricao,
            "concluida": tarefa.concluida,
        }
        for tarefa in tarefas
    ]
    if not tarefas_pagina:
        raise HTTPException(
            status_code=404, detail="Nenhuma tarefa encontrada nesta página"
        )
    return {
        "page": page,
        "size": size,
        "total": len(tarefas),
        "tarefas": tarefas_pagina,
    }


@app.put("/concluir_tarefa/{nome_tarefa}")
def concluir_tarefa(
    nome_tarefa: str,
    db: SessionLocal = Depends(get_db),
    credentials: HTTPBasicCredentials = Depends(authenticate),
):
    tarefa = db.query(TarefaDB).filter(TarefaDB.nome == nome_tarefa).first()
    if tarefa:
        tarefa.concluida = True
        db.commit()
        db.refresh(tarefa)
        return {"message": f"Tarefa {nome_tarefa} concluída com sucesso!"}
    raise HTTPException(status_code=404, detail=f"Tarefa {nome_tarefa} não encontrada")


@app.delete("/remover_tarefa/{nome_tarefa}")
def remover_tarefa(
    nome_tarefa: str,
    db: SessionLocal = Depends(get_db),
    credentials: HTTPBasicCredentials = Depends(authenticate),
):
    tarefa = db.query(TarefaDB).filter(TarefaDB.nome == nome_tarefa).first()
    if tarefa:
        db.delete(tarefa)
        db.commit()
        return {"message": f"Tarefa {nome_tarefa} removida com sucesso!"}
    raise HTTPException(status_code=404, detail=f"Tarefa {nome_tarefa} não encontrada")
