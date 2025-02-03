FROM python:3.11-slim
LABEL maintainer="adamj"

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-root

COPY ./ /app/

ENV PYTHONPATH=/app

CMD ["python3", "./report/main.py"]
