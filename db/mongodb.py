import pymongo

from configs import DB_NAME, MONGO_URL


def get_database():
    client = pymongo.MongoClient(MONGO_URL, 27017)
    return client[DB_NAME]