FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y default-mysql-client \
    && pip install -r requirements.txt

ENV FLASK_APP=app.py
EXPOSE 5000

CMD ["python", "./app.py"]

