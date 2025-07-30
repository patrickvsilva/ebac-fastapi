from fastapi import FastAPI, HTTPException


app = FastAPI()

tarefas = []


@app.post("/adicionar_tarefa")
def read_root(nome_tarefa: str, descricao_tarefa: str):
    if any(tarefa["nome"] == nome_tarefa for tarefa in tarefas):
        raise HTTPException(status_code=400, detail=f"Tarefa {nome_tarefa} já existe")
    tarefas.append(
        {"nome": nome_tarefa, "descrição": descricao_tarefa, "concluída": False}
    )
    return f"Tarefa {nome_tarefa} adicionada com sucesso!"


@app.get("/listar_tarefas")
def listar_tarefas():
    if not tarefas:
        return {"message": "Nenhuma tarefa encontrada"}
    return {"tarefas": tarefas}


@app.put("/concluir_tarefa/{nome_tarefa}")
def concluir_tarefa(nome_tarefa: str):
    for tarefa in tarefas:
        if tarefa["nome"] == nome_tarefa:
            tarefa["concluída"] = True
            return {"message": f"Tarefa {nome_tarefa} concluída com sucesso!"}
    raise HTTPException(status_code=404, detail=f"Tarefa {nome_tarefa} não encontrada")


@app.delete("/remover_tarefa/{nome_tarefa}")
def remover_tarefa(nome_tarefa: str):
    tarefas[:] = [tarefa for tarefa in tarefas if tarefa["nome"] != nome_tarefa]
    return {"message": f"Tarefa {nome_tarefa} removida com sucesso!"}
