# API-Tarefas

## Como executar o projeto localmente

1. Clone o repositório:
    ```bash
    git clone https://github.com/seu-usuario/ebac-fastapi.git
    cd ebac-fastapi
    ```

2. Instale o Poetry (gerenciador de dependências):
    ```bash
    pip install poetry
    ```

3. Instale as dependências do projeto:
    ```bash
    poetry install
    ```

4. Inicie a aplicação:
    ```bash
    uvicorn main:app --reload
    ```

5. Para parar a aplicação, pressione `Ctrl+C` no terminal onde ela está rodando.

6. Acesse a documentação interativa em [http://localhost:8000/docs](http://localhost:8000/docs).

---

## Executando com Docker Compose

1. Certifique-se de que o Docker e o Docker Compose estão instalados em sua máquina.

2. Inicie os serviços com o comando:
    ```bash
    docker compose up
    ```

3. Para parar os serviços, utilize:
    ```bash
    docker compose down
    ```

4. Acesse a aplicação em [http://localhost:8000](http://localhost:8000) e a documentação em [http://localhost:8000/docs](http://localhost:8000/docs).