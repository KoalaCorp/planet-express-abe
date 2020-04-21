# coding=utf-
from flask import Flask
from flask_cors import CORS

import json

from mongo import Mongo
from settings import (IP_HOST, PORT_HOST, MONGO_HOST, MONGO_PORT,
                      MONGO_DATABASE, DOMAIN)




app = Flask(__name__)
CORS(app)


@app.route('/api/<collection>/<query>', methods=['GET'])
def get_relations(collection, query):
    mongo_instance = Mongo(MONGO_DATABASE, MONGO_HOST, MONGO_PORT)
    return json.dumps(mongo_instance.get_relations(collection,
                                                   query.split(",")))


@app.route('/api/<collection>/<query>/<scores>', methods=['GET'])
def get_relations_scores(collection, query, scores):
    mongo_instance = Mongo(MONGO_DATABASE, MONGO_HOST, MONGO_PORT)
    queries = query.split(",")
    scores = scores.split(",")
    if len(queries) != len(scores):
        raise BaseException("Distinct size of elements")
    elif not all(isinstance(int(score), int) for score in scores):
        raise BaseException("Scores are not int")

    return json.dumps(mongo_instance.get_relations_scores(collection,
                                                          queries,
                                                          scores))


@app.route('/api/topics/<collection>/<query>', methods=['GET'])
def get_relations_topics(collection, query):
    mongo_instance = Mongo(MONGO_DATABASE, MONGO_HOST, MONGO_PORT)
    queries = query.split(",")

    return json.dumps(mongo_instance.get_relations_topics(collection,
                                                          queries))


@app.route('/api/sources', methods=['GET'])
def get_sources():
    mongo_instance = Mongo(MONGO_DATABASE, MONGO_HOST, MONGO_PORT)

    json_response = {
      "links": {
        "self": "http://{}:{}/sources".format(DOMAIN, PORT_HOST)
      },
      "data": mongo_instance.get_sources(),
      "jsonapi": {
        "version": "1.0"
      }
    }

    return json.dumps(json_response)


if __name__ == '__main__':
    app.debug = True
    app.run(IP_HOST, PORT_HOST)
