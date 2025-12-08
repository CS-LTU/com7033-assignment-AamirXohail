from flask import current_app, g
from pymongo import MongoClient


def get_mongo_client():
    if "mongo_client" not in g:
        uri = current_app.config["MONGO_URI"]
        g.mongo_client = MongoClient(uri)
    return g.mongo_client


def get_mongo_db():
    client = get_mongo_client()
    db_name = current_app.config["MONGO_DB_NAME"]
    return client[db_name]


def close_mongo_client(e=None):
    client = g.pop("mongo_client", None)
    if client is not None:
        client.close()
