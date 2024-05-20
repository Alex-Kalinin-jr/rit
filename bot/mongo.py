import datetime
from pprint import pprint
import pymongo

from pymongo import MongoClient

client = MongoClient("localhost", 27017)

db = client["sample_db"]
collection = db['sample_collection']


def find_records(start: datetime, end: datetime):
    records = collection.find({
        "dt": {
            "$gte": start,
            "$lte": end
        }
    })
    for record in records:
        print(record)

    return records

def main():
    find_records(datetime.datetime(2022, 12, 31, 14, 1), datetime.datetime(2022, 12, 31, 17, 1))

if __name__ == "__main__":
    main()