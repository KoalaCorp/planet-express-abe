# coding=utf-8
import os

# FLASK VARS
IP_HOST = os.getenv("IP_HOST", "0.0.0.0")
DOMAIN = os.getenv("DOMAIN", "localhost")
PORT_HOST = os.getenv("PORT_HOST", 5000)

MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = os.getenv("MONGO_PORT", 27017)
MONGO_DATABASE = os.getenv("MONGO_DATABASE", "planet-express")


API_VERSION = "1.0"


# Testing
MONGO_DATABASE_TESTS = os.getenv("MONGO_DATABASE_TESTS", "planet-express-tests")
