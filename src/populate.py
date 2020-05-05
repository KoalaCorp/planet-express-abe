import argparse
import json

from mongo import Mongo


def populate(mongo_database, mongo_host, mongo_port):
    mongo_instance = Mongo(mongo_database, mongo_host, mongo_port)
    collection = mongo_instance.database['sources']
    with open('configuration/data_sources.json') as data_sources_file:
        data_sources = json.load(data_sources_file)
        for source in data_sources:
            collection.replace_one({'id': source['id']}, source, upsert=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Populate the database whit initial data')
    parser.add_argument('--mongo_database', help='Mongo database name')
    parser.add_argument('--mongo_host', help='Type of text to tokenize',
                        default='text')
    parser.add_argument('--mongo_port', help='PDF paragraph text separator',
                        default='  \x0c')
    args = parser.parse_args()
    populate(args.mongo_database, args.mongo_host, args.mongo_port)
