# coding=utf-8
import os

# FLASK VARS
IP_HOST = "0.0.0.0"
PORT_HOST = 5000

MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = os.getenv("MONGO_PORT", 27017)
MONGO_DATABASE = os.getenv("MONGO_DATABASE", "planet-express")
