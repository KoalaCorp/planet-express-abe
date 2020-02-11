from pymongo import MongoClient


class Mongo(object):
    def __init__(self, database, host, port):
        client = MongoClient(host, port)
        self.database = client[database]

    def get_relations(self, collection, query):
        collection = self.database[collection]
        return [doc for doc in
                collection.find({"tokenized.word": {"$in": query}},
                                {'_id': False})]

    def get_relations_scores(self, collection, queries, scores):
        collection = self.database[collection]
        iterator_docs = collection.find({"tokenized.word": {"$in": queries}},
                                        {'_id': False})
        queries_scores = {
            query: int(score) for query, score in zip(queries, scores)}

        docs = []
        for doc in iterator_docs:
            enough_score = False
            for querie, score in queries_scores.items():
                for item in doc['tokenized']:
                    if item["word"] == querie and item["score"] >= score:
                        enough_score = True
                        break
            if enough_score:
                docs.append(doc)

        affinities = {}
        for doc1 in docs:
            for doc2 in docs:
                if doc1['url'] != doc2['url'] and\
                   (doc2['url'] not in affinities.keys() or
                    (doc2['url'] in affinities.keys() and
                     doc1['url'] not in affinities[doc2['url']].keys())):
                    if len(doc1['tokenized']) < len(doc2['tokenized']):
                        tokenized_list1 = doc1['tokenized']
                        tokenized_list2 = doc2['tokenized']
                    else:
                        tokenized_list1 = doc2['tokenized']
                        tokenized_list2 = doc1['tokenized']
                    affinity_words = []
                    for item1 in tokenized_list1:
                        for item2 in tokenized_list2:
                            if item1['word'] == item2['word']:
                                affinity_words.append(
                                    {
                                        item1['word']:
                                            abs(
                                                item1['score'] - item2['score']
                                                )})
                    if affinity_words:
                        affinities.setdefault(doc1['url'], {}).setdefault(doc2['url'], affinity_words)
                        affinities.setdefault(doc2['url'], {}).setdefault(doc1['url'], affinity_words)

        return affinities
