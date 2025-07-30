from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import secrets

app = FastAPI()

USER = "admin"
PASSWORD = "admin"

security = HTTPBasic()

tarefas = []


def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    is_user_correct = secrets.compare_digest(credentials.username, USER)
    is_password_correct = secrets.compare_digest(credentials.password, PASSWORD)

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
    tarefa: Tarefa, credentials: HTTPBasicCredentials = Depends(authenticate)
):
    if any(t.nome == tarefa.nome for t in tarefas):
        raise HTTPException(status_code=400, detail=f"Tarefa {tarefa.nome} já existe")
    tarefas.append(tarefa)
    return {"message": f"Tarefa {tarefa.nome} adicionada com sucesso!"}


@app.get("/listar_tarefas")
def listar_tarefas(credentials: HTTPBasicCredentials = Depends(authenticate)):
    if not tarefas:
        return {"message": "Nenhuma tarefa encontrada"}
    return {"tarefas": [tarefa.dict() for tarefa in tarefas]}


@app.put("/concluir_tarefa/{nome_tarefa}")
def concluir_tarefa(
    nome_tarefa: str, credentials: HTTPBasicCredentials = Depends(authenticate)
):
    for tarefa in tarefas:
        if tarefa.nome == nome_tarefa:
            tarefa.concluida = True
            return {"message": f"Tarefa {nome_tarefa} concluída com sucesso!"}
    raise HTTPException(status_code=404, detail=f"Tarefa {nome_tarefa} não encontrada")


@app.delete("/remover_tarefa/{nome_tarefa}")
def remover_tarefa(
    nome_tarefa: str, credentials: HTTPBasicCredentials = Depends(authenticate)
):
    tarefas[:] = [tarefa for tarefa in tarefas if tarefa.nome != nome_tarefa]
    return {"message": f"Tarefa {nome_tarefa} removida com sucesso!"}
