FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["fastapi", "run", "app/main.py", "--port", "80"]