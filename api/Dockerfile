FROM python:3.11-slim

RUN apt-get update && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# COPIE TOUT le code (main.py + anilist/ + web/)
COPY . .
COPY alembic.ini .
COPY alembic ./alembic


EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
