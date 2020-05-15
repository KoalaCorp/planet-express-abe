import json
import unittest

from mongo import SourcesMongo, SourceMongo, LinksTopicsMongo
from populate import populate
from settings import MONGO_HOST, MONGO_PORT, MONGO_DATABASE_TESTS


def populate_db_tests():
    populate(MONGO_DATABASE_TESTS, MONGO_HOST, MONGO_PORT)


class LinksTopicsMongoTestCase(unittest.TestCase):
    source = "elfarodeceuta"

    @classmethod
    def setUpClass(cls):
        populate_db_tests()
        cls.mongo_instance = LinksTopicsMongo(MONGO_DATABASE_TESTS,
                                              MONGO_HOST, MONGO_PORT,
                                              ('topics', 'names'))
        collection = cls.mongo_instance.database[cls.source]
        with open('tests/mongo_test.json') as json_file:
            json_data = json.load(json_file)
            for data in json_data:
                collection.insert(data)

    @classmethod
    def tearDownClass(cls):
        cls.mongo_instance.database[cls.source].remove({})

    def test_get_links_topics(self):
        topics, links = LinksTopicsMongoTestCase.mongo_instance.\
            get_links_topics(self.source, ["ceuta"], 2)
        topics_expected = [
          {
            "type": "topics",
            "id": "ceuta",
            "attributes": {
              "label": "ceuta"
            },
            "meta": {
              "counter": 12
            }
          },
          {
            "type": "topics",
            "id": "pp",
            "attributes": {
              "label": "pp"
            },
            "meta": {
              "counter": 12
            }
          },
          {
            "type": "topics",
            "id": "vivas",
            "attributes": {
              "label": "vivas"
            },
            "meta": {
              "counter": 18
            }
          },
          {
            "type": "topics",
            "id": "ayuntamiento",
            "attributes": {
              "label": "ayuntamiento"
            },
            "meta": {
              "counter": 12
            }
          }
        ]
        self.assertEqual(topics, topics_expected)
        print(links)
        links_expected = [
          {
            "endpoints": [
              "ceuta",
              "pp"
            ],
            "urls": [
              {
                "title": "Data source with ceuta and pp",
                "date": "02/05/2020",
                "href": "https://elfarodeceuta.es/1",
                "source": {
                  "label": "elfarodeceuta",
                  "name": "El Faro de Ceuta"
                }
              }
            ]
          },
          {
            "endpoints": [
              "ceuta",
              "vivas"
            ],
            "urls": [
              {
                "title": "Data source with vivas, ayuntamiento, ceuta",
                "date": "02/05/2020",
                "href": "https://elfarodeceuta.es/4",
                "source": {
                  "label": "elfarodeceuta",
                  "name": "El Faro de Ceuta"
                }
              }
            ]
          },
          {
            "endpoints": [
              "ceuta",
              "ayuntamiento"
            ],
            "urls": [
              {
                "title": "Data source with vivas, ayuntamiento, ceuta",
                "date": "02/05/2020",
                "href": "https://elfarodeceuta.es/4",
                "source": {
                  "label": "elfarodeceuta",
                  "name": "El Faro de Ceuta"
                }
              }
            ]
          },
          {
            "endpoints": [
              "vivas",
              "ayuntamiento"
            ],
            "urls": [
              {
                "title": "Data source with vivas, ayuntamiento, ceuta",
                "date": "02/05/2020",
                "href": "https://elfarodeceuta.es/4",
                "source": {
                  "label": "elfarodeceuta",
                  "name": "El Faro de Ceuta"
                }
              },
              {
                "title": "Data source with vivas and ayuntamiento",
                "date": "02/05/2020",
                "href": "https://elfarodeceuta.es/3",
                "source": {
                  "label": "elfarodeceuta",
                  "name": "El Faro de Ceuta"
                }
              }
            ]
          },
          {
            "endpoints": [
              "pp",
              "vivas"
            ],
            "urls": [
              {
                "title": "Data source with pp and vivas",
                "date": "02/05/2020",
                "href": "https://elfarodeceuta.es/2",
                "source": {
                  "label": "elfarodeceuta",
                  "name": "El Faro de Ceuta"
                }
              }
            ]
          }
        ]
        self.assertEqual(links, links_expected)


class SourcesMongoTestCase(unittest.TestCase):
    def setUp(self):
        populate(MONGO_DATABASE_TESTS, MONGO_HOST, MONGO_PORT)

    def test_get_sources(self):
        mongo_instance = SourcesMongo(MONGO_DATABASE_TESTS,
                                      MONGO_HOST, MONGO_PORT)
        response = [
            {
              "type": "source",
              "id": "elfarodeceuta",
              "attributes": {
                "label": "elfarodeceuta",
                "name": "El Faro de Ceuta",
                "url": "https://elfarodeceuta.es/"
              }
            },
            {
              "type": "source",
              "id": "elpueblodeceuta",
              "attributes": {
                "label": "elpueblodeceuta",
                "name": "El pueblo de Ceuta",
                "url": "https://elpueblodeceuta.es/"
              }
            },
            {
              "type": "source",
              "id": "bocce",
              "attributes": {
                "label": "bocce",
                "name": "Boletin Oficial Ciudad De Ceuta",
                "url": "http://www.ceuta.es/ceuta/bocce"
              }
            }
          ]
        self.assertEqual(mongo_instance.get_sources(), response)


class SourceMongoTestCase(unittest.TestCase):
    def setUp(self):
        populate(MONGO_DATABASE_TESTS, MONGO_HOST, MONGO_PORT)

    def test_get_source(self):
        mongo_instance = SourceMongo(MONGO_DATABASE_TESTS,
                                     MONGO_HOST, MONGO_PORT)
        response = {
              "type": "source",
              "id": "elfarodeceuta",
              "attributes": {
                "label": "elfarodeceuta",
                "name": "El Faro de Ceuta",
                "url": "https://elfarodeceuta.es/"
              }
            }
        self.assertEqual(mongo_instance.get_source("elfarodeceuta"), response)


if __name__ == '__main__':
    unittest.main()
