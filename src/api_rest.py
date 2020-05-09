# coding=utf-
import json

from flask import Flask, jsonify
from flask_cors import CORS


from mongo import Mongo, LinksTopicsMongo, SourcesMongo, SourceMongo
from settings import (IP_HOST, PORT_HOST, MONGO_HOST, MONGO_PORT,
                      MONGO_DATABASE, DOMAIN, API_VERSION)


app = Flask(__name__)
CORS(app)

API_BASE_DOMAIN = "http://{}:{}/api".format(DOMAIN, PORT_HOST)


@app.route('/api/sources/<source_name>/topics/<topics>/degrees/<degrees>',
           methods=['GET'])
@app.route('/api/sources/<source_name>/topics/<topics>',
           defaults={'degrees': 2},
           methods=['GET'])
def get_links_topics(source_name, topics, degrees):
    mongo_instance = LinksTopicsMongo(MONGO_DATABASE, MONGO_HOST, MONGO_PORT)
    queries = topics.split(",")
    topics_nodes, links = mongo_instance.get_links_topics(source_name, queries,
                                                          degrees)
    json_response = {
        "links": {
            "self": "{}/sources/{}/topics/{}/degrees/{}".format(API_BASE_DOMAIN,
                                                                source_name,
                                                                topics,
                                                                degrees)
        },
        "data": topics_nodes,
        "meta": {
            "links": links
        },
        "jsonapi": {
            "version": API_VERSION
        }
    }

    return jsonify(json_response)


@app.route('/api/sources', methods=['GET'])
def get_sources():
    mongo_instance = SourcesMongo(MONGO_DATABASE, MONGO_HOST, MONGO_PORT)

    json_response = {
      "links": {
        "self": "{}/sources".format(API_BASE_DOMAIN)
      },
      "data": mongo_instance.get_sources(),
      "jsonapi": {
        "version": API_VERSION
      }
    }

    return jsonify(json_response)


@app.route('/api/sources/<source>', methods=['GET'])
def get_source(source):
    mongo_instance = SourceMongo(MONGO_DATABASE, MONGO_HOST, MONGO_PORT)

    json_response = {
      "links": {
        "self": "{}/sources/{}".format(API_BASE_DOMAIN, source)
      },
      "data": mongo_instance.get_source(source),
      "jsonapi": {
        "version": API_VERSION
      }
    }

    return jsonify(json_response)


if __name__ == '__main__':
    app.debug = True
    app.run(IP_HOST, PORT_HOST)
