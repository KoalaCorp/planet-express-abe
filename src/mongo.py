from pymongo import MongoClient


class Mongo(object):
    def __init__(self, database, host, port):
        self.client = MongoClient(host, port)
        self.database = self.client[database]


class SourcesMongo(Mongo):
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


class SourceMongo(Mongo):
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


class LinksTopicsMongo(Mongo):
    date_time = "date_time"
    title = "title"

    def __init__(self, database, host, port, sections):
        self.sections = sections
        self.links_dict = {}
        self.topics_dict = {}
        self.exclude_ids = []
        self.queries = None
        Mongo.__init__(self, database, host, port)

    def __doc_to_url(self, doc, source_data):
        doc_keys = doc.keys()
        return {
            self.title: doc[self.title] if self.title in doc_keys else "",
            "date": doc[self.date_time] if self.date_time in doc_keys else "",
            "href": doc['url'],
            "source": {
                "label": source_data["id"],
                "name": source_data["name"]
            }
        }

    def __doc_to_topic__(self, topic_word, score):
        return {
            "type": "topics",
            "id": topic_word,
            "attributes": {
                "label": topic_word
            },
            "meta": {
                "counter": score
            }
        }

    def __doct_to_link__(self, sorted_topics_name_list, url):
        return {
            "endpoints": sorted_topics_name_list,
            "urls": [url]
        }

    def __iterate_docs__(self, iterator_docs, source_data):
        for doc in iterator_docs:
            self.exclude_ids.append(doc['_id'])
            url = self.__doc_to_url(doc, source_data)
            for token in doc['tokenized']:
                url_topics = []
                for section in self.sections:
                    for topic in token[section]:
                        topic_word = topic['word']
                        self.queries.append(topic_word)
                        for url_topic in url_topics:
                            sorted_topics_name_list = [url_topic, topic_word]
                            sorted_topics_name = "_".join(sorted_topics_name_list)
                            if sorted_topics_name not in self.links_dict.keys():
                                self.links_dict[sorted_topics_name] =\
                                    self.__doct_to_link__(sorted_topics_name_list,
                                                          url)
                            else:
                                self.links_dict[sorted_topics_name]["urls"]\
                                    .append(url)
                        url_topics.append(topic_word)

                        if topic_word not in self.topics_dict.keys():
                            self.topics_dict[topic_word] =\
                                self.__doc_to_topic__(topic_word, topic['score'])
                        else:
                            self.topics_dict[topic['word']]['meta']['counter'] +=\
                                topic['score']

    def get_links_topics(self, source, queries, degrees):
        sources_collection = self.database['sources']
        source_data = sources_collection.find_one({"id": source})
        collection = self.database[source]
        self.queries = queries

        for degree in range(degrees):
            regex_query = "|".join(self.queries) if len(self.queries) > 1 else self.queries[-1]
            or_query = [{
                "tokenized.{}.word".format(tokenized_section): {
                    "$regex": regex_query,
                    "$options": "i"
                }
            } for tokenized_section in self.sections]
            iterator_docs = collection.find(
                {
                    "_id": {"$nin": self.exclude_ids},
                    "$or": or_query
                }
            )
            self.__iterate_docs__(iterator_docs, source_data)

        links = [val for key, val in self.links_dict.items()]
        topics = [val for key, val in self.topics_dict.items()]
        return topics, links
