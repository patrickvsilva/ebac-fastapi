from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()

tarefas = []


class Tarefa(BaseModel):
    nome: str
    descricao: str
    concluida: bool = False


@app.post("/adicionar_tarefa")
def read_root(tarefa: Tarefa):
    if any(t["nome"] == tarefa.nome for t in tarefas):
        raise HTTPException(status_code=400, detail=f"Tarefa {tarefa.nome} já existe")
    tarefas.append(tarefa.dict())
    return {"message": f"Tarefa {tarefa.nome} adicionada com sucesso!"}


@app.get("/listar_tarefas")
def listar_tarefas():
    if not tarefas:
        return {"message": "Nenhuma tarefa encontrada"}
    return {"tarefas": tarefas}


@app.put("/concluir_tarefa/{nome_tarefa}")
def concluir_tarefa(nome_tarefa: str):
    for tarefa in tarefas:
        if tarefa["nome"] == nome_tarefa:
            tarefa["concluida"] = True
            return {"message": f"Tarefa {nome_tarefa} concluída com sucesso!"}
    raise HTTPException(status_code=404, detail=f"Tarefa {nome_tarefa} não encontrada")


@app.delete("/remover_tarefa/{nome_tarefa}")
def remover_tarefa(nome_tarefa: str):
    tarefas[:] = [tarefa for tarefa in tarefas if tarefa["nome"] != nome_tarefa]
    return {"message": f"Tarefa {nome_tarefa} removida com sucesso!"}
