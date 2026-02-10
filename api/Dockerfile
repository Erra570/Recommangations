FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# COPIE TOUT le code (main.py + anilist/ + web/)
COPY . .
COPY alembic.ini .
COPY alembic ./alembic


EXPOSE 8000

#http
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
#https
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--ssl-keyfile", "key.pem", "--ssl-certfile", "cert.pem"]
