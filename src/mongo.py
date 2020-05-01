from pymongo import MongoClient


class Mongo(object):
    def __init__(self, database, host, port):
        client = MongoClient(host, port)
        self.database = client[database]

    def get_links_topics(self, source, queries):
        sources_collection = self.database['sources']
        source_data = sources_collection.find_one({"id": source}, {'_id': False})
        collection = self.database[source]
        iterator_docs = collection.find(
            {
                "$or": [
                    {"tokenized.topics.word": {"$in": queries}},
                    {"tokenized.names.word": {"$in": queries}}
                ]
            },
            {'_id': False}
        )

        links_dict = {}
        topics_dict = {}
        date_time = "date_time"
        title = "title"
        for doc in iterator_docs:
            doc_keys = doc.keys()
            url = {
                title: doc[title] if title in doc_keys else "",
                "date": doc[date_time] if date_time in doc_keys else "",
                "href": doc['url'],
                "source": {
                    "label": source_data["id"],
                    "name": source_data["name"]
                }
            }
            for token in doc['tokenized']:
                url_topics = []
                for topic in token['topics']:
                    topic_word = topic['word']
                    topic_keys = topics_dict.keys()
                    links_keys = links_dict.keys()

                    for url_topic in url_topics:
                        sorted_topics_name_list = [url_topic, topic_word]
                        sorted_topics_name = "_".join(sorted_topics_name_list)
                        if sorted_topics_name not in links_keys:
                            links_dict[sorted_topics_name] = {
                                "endpoints": sorted_topics_name_list,
                                "urls": [url]
                            }
                        else:
                            links_dict[sorted_topics_name]["urls"].append(url)
                    url_topics.append(topic_word)

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


        links = [val for key, val in links_dict.items()]
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

    def get_source(self, source):
        collection = self.database['sources']
        source_data = collection.find_one({"id": source}, {'_id': False})

        return_data = {
            "type": "source",
            "id": source_data['id'],
            "attributes": {
                "label": source_data['id'],
                "name": source_data['name'],
                "url": source_data['home']
            }
        }

        return return_data
