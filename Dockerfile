#syntax=docker/dockerfile:1.4

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

CMD ["gunicorn", "main:app", "-b", "unix:/app-socket/async.sock", "-w", "4", "-k", "uvicorn.workers.UvicornWorker"]
