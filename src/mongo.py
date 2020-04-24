from pymongo import MongoClient


class Mongo(object):
    def __init__(self, database, host, port):
        client = MongoClient(host, port)
        self.database = client[database]

    def get_links_topics(self, collection, queries):
        collection = self.database[collection]
        iterator_docs = collection.find(
            {
            "tokenized.topics.word": {
                "$in": queries
                }
            },
            {'_id': False}
        )
        links = {}
        topics_dict = {}
        url_topics = []
        for doc in iterator_docs:
            for token in doc['tokenized']:
                url_topics = []
                for topic in token['topics']:
                    topic_word = topic['word']
                    topic_keys = topics_dict.keys()
                    topic_word_not_in_topic_keys = bool(topic_word not in topic_keys)

                    # for url_topic in url_topics:
                    #     if url_topic not in topic_keys or topic_word_not_in_topic_keys:
                    #         links.append({'from': topic_word, 'to': url_topic})
                    # url_topics.append(topic_word)

                    if topic_word not in topic_keys:
                        topics_dict[topic_word] = {
                            "type": "topics",
                            "id": topic_word,
                            "attributes": {
                                "label": topic_word
                            },
                            "meta": {
                                "counter": topic['score']
                            }
                        }
                    else:
                        topics_dict[topic['word']]['meta']['counter'] += topic['score']



        topics = [val for key, val in topics_dict.items()]
        return topics, links

    def get_sources(self):
        collection = self.database['sources']
        iterator_docs = collection.find({}, {'_id': False})
        data = [
            {
                "type": "source",
                "id": source['id'],
                "attributes": {
                    "label": source['id'],
                    "name": source['name'],
                    "url": source['home']
                }
            } for source in iterator_docs
          ]

        return data
