FROM python:3.11-slim

RUN apt-get update
<<<<<<< HEAD
# On retire les fichiers temporaires :
=======
#  On retire les fichiers temporaires :
>>>>>>> f985981 (appel graphql)
RUN rm -rf /var/lib/apt/lists/* 

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]