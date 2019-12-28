import os

from pymongo import MongoClient

__SECRET_PW = os.environ.get('MONGO_INITDB_ROOT_USERNAME')
__SECRET_UNAME = os.environ.get('MONGO_INITDB_ROOT_PASSWORD')


def get_mongo_client() -> MongoClient:
    return MongoClient(
        host=f'mongodb://{__SECRET_UNAME}:{__SECRET_PW}@db',
        connect=False,
    )
