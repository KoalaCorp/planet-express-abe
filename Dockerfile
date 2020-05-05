FROM python:3.6.2-slim

ENV RABBITMQ_HOST rabbitmq
ENV MONGO_HOST mongo

ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
ADD src /api
