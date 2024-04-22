FROM python:3.11-slim
LABEL maintainer="adamj"

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock /app/

COPY ./ /app/


RUN poetry config virtualenvs.create false \
    &&poetry install

CMD ["python3", "./raport/main.py"]
