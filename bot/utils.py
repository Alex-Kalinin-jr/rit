import datetime
import pymongo
from pymongo import MongoClient
from models import MessageData

def find_records(data: MessageData, collection):
    records = collection.find({
        "dt": {
            "$gte": data.dt_from,
            "$lte": data.dt_upto
        }
    })
    return records


def aggregate(data: MessageData, collection):
    records = find_records(data, collection)
    