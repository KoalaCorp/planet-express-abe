FROM python:3.6.2-slim

ENV RABBITMQ_HOST rabbitmq
ENV MONGO_HOST mongo

ADD requeriments.txt /requeriments.txt
RUN pip install -r /requeriments.txt
ADD src /api
