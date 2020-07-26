FROM python:3.8-alpine

COPY ./src/publish.py app/app.py

WORKDIR /app

RUN pip install pika

CMD ["python", "app.py"]
