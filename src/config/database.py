import os
from pymongo import MongoClient


def get_database():
    connection_string = os.getenv("MONGO_CONNECTION_STRING")
    client = MongoClient(connection_string)

    return client["the_noble_concierge"]
