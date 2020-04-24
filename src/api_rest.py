# coding=utf-
from flask import Flask
from flask_cors import CORS

import json

from mongo import Mongo
from settings import (IP_HOST, PORT_HOST, MONGO_HOST, MONGO_PORT,
                      MONGO_DATABASE, DOMAIN, API_VERSION)


app = Flask(__name__)
CORS(app)

API_BASE_DOMAIN =  "http://{}:{}/api".format(DOMAIN, PORT_HOST)


@app.route('/api/sources/<source_name>/topics/<topics>', methods=['GET'])
def get_links_topics(source_name, topics):
    mongo_instance = Mongo(MONGO_DATABASE, MONGO_HOST, MONGO_PORT)
    queries = topics.split(",")
    topics_nodes, links = mongo_instance.get_links_topics(source_name, queries)
    json_response = {
        "links": {
            "self": "{}/sources/{}/topics/{}".format(API_BASE_DOMAIN,
                                                     source_name,
                                                     topics)
        },
        "data": topics_nodes,
        "meta": {
            "links": links
        },
        "jsonapi": {
            "version": API_VERSION
        }
    }

    return json.dumps(json_response)


@app.route('/api/sources', methods=['GET'])
def get_sources():
    mongo_instance = Mongo(MONGO_DATABASE, MONGO_HOST, MONGO_PORT)

    json_response = {
      "links": {
        "self": "{}/sources".format(API_BASE_DOMAIN)
      },
      "data": mongo_instance.get_sources(),
      "jsonapi": {
        "version": API_VERSION
      }
    }

    return json.dumps(json_response)

@app.route('/api/sources/<source>', methods=['GET'])
def get_source(source):
    mongo_instance = Mongo(MONGO_DATABASE, MONGO_HOST, MONGO_PORT)

    json_response = {
      "links": {
        "self": "{}/sources/{}".format(API_BASE_DOMAIN, source)
      },
      "data": mongo_instance.get_source(source),
      "jsonapi": {
        "version": API_VERSION
      }
    }

    return json.dumps(json_response)


if __name__ == '__main__':
    app.debug = True
    app.run(IP_HOST, PORT_HOST)
