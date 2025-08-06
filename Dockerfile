FROM python:3.10-slim

WORKDIR /app
RUN pip install poetry
COPY app.py README.md poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-root
COPY app.py ./
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]