FROM python:3.9.9
RUN mkdir -p /todo_app
WORKDIR /todo_app
COPY . .
RUN ls -la
RUN apt-get update
RUN apt-get install -y  --no-install-recommends --no-install-suggests gcc autoconf libc6-dev curl libssl-dev libffi-dev
RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root
CMD ["poetry", "run", "uvicorn", "src.app:fast_api","--host=0.0.0.0", "--port=28002", "--log-level=debug", "--workers=1", "--timeout-keep-alive=60"]