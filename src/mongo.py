from pymongo import MongoClient


class Mongo(object):
    def __init__(self, database, host, port):
        client = MongoClient(host, port)
        self.database = client[database]

    def get_relations(self, collection, query):
        collection = self.database[collection]
        return [doc for doc in
                collection.find({"tokenized.topics.word": {"$in": query}},
                                {'_id': False})]

    def get_relations_scores(self, collection, queries, scores):
        collection = self.database[collection]
        iterator_docs = collection.find({"tokenized.topics.word": {"$in": queries}},
                                        {'_id': False})
        queries_scores = {
            query: int(score) for query, score in zip(queries, scores)}

        docs = []
        for doc in iterator_docs:
            enough_score = False
            for querie, score in queries_scores.items():
                for token_item in doc['tokenized']:
                    for item in token_item['topics']:
                        if item["word"] == querie and item["score"] >= score:
                            enough_score = True
                            break
                    if enough_score:
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
                    doc1_flatt = [word for token_item in doc1['tokenized'] for word in token_item['topics']]
                    doc2_flatt = [word for token_item in doc2['tokenized'] for word in token_item['topics']]
                    if len(doc1_flatt) < len(doc2_flatt):
                        tokenized_list1 = doc1_flatt
                        tokenized_list2 = doc2_flatt
                    else:
                        tokenized_list1 = doc2_flatt
                        tokenized_list2 = doc1_flatt
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
                        affinities.setdefault(doc1['url'],
                                              {'date_time': doc1['date_time'] if 'date_time' in doc1.keys() else None}).\
                                   setdefault(doc2['url'],
                                              {'date_time': doc2['date_time'] if 'date_time' in doc2.keys() else None,
                                               'affinity_words': affinity_words})
                        affinities.setdefault(doc2['url'],
                                              {'date_time': doc2['date_time'] if 'date_time' in doc2.keys() else None}).\
                                   setdefault(doc1['url'],
                                              {'date_time': doc1['date_time'] if 'date_time' in doc1.keys() else None,
                                               'affinity_words': affinity_words})

        return affinities

    def get_relations_topics(self, collection, queries):
        collection = self.database[collection]
        iterator_docs = collection.find({"tokenized.topics.word": {"$in": queries}},
                                        {'_id': False})
        edges = []
        topics_dict = {}
        url_topics = []
        for doc in iterator_docs:
            for token in doc['tokenized']:
                url_topics = []
                for topic in token['topics']:
                    topic_word = topic['word']
                    topic_keys = topics_dict.keys()
                    topic_word_not_in_topic_keys = bool(topic_word not in topic_keys)

                    for url_topic in url_topics:
                        if url_topic not in topic_keys or topic_word_not_in_topic_keys:
                            edges.append({'from': topic_word, 'to': url_topic})
                    url_topics.append(topic_word)

                    if topic_word not in topic_keys:
                        topics_dict[topic_word] = {'id': topic_word,
                                                   'label': topic_word,
                                                   'urls': [doc['url']]}
                    else:
                        topics_dict[topic['word']]['urls'].append(doc['url'])



        topics = [val for key, val in topics_dict.items()]
        return {'topics': topics, 'edges': edges}

    def get_sources(self):
        collection = self.database['sources']
        iterator_docs = collection.find({}, {'_id': False})
        data = [
            {
            "type": "collection",
            "attributes": {
                "collection": source['id'],
                "name": source['name']
                },
            "links": {
                "self": source['home']
                }
            } for source in iterator_docs
          ]

        return data
