FROM python:3.11-buster

ENV TZ Asia/Tokyo
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install poetry


COPY pyproject.toml* poetry.lock* ./


RUN poetry config virtualenvs.in-project true
RUN if [ -f pyproject.toml ]; then poetry install --no-root; fi

# uvicornのサーバーを立ち上げる
ENTRYPOINT ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--reload"]
