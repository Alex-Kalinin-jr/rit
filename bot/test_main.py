import sys
import os

from pymongo import MongoClient

from utils import aggregate
from models import *

module_dir = '.'
sys.path.append(module_dir)


client = MongoClient("mongodb://localhost:27017")
db = client["sample_db"]
collection = db['sample_collection']


def test_aggregate(collection):
    message_data = MessageData(dt_from=datetime.strptime("2022-09-01T00:00:00", "%Y-%m-%dT%H:%M:%S"),
                            dt_upto=datetime.strptime("2022-12-31T23:59:00", "%Y-%m-%dT%H:%M:%S"),
                            group_type='month')
    print('i am here-----------------')
    result = aggregate(message_data, collection)
    print('and here-----------------')
    print(result)
    # assert result == {
    #     "dataset": [5906586, 5515874, 5889803, 6092634],
    #     "labels": ["2022-09-01T00:00:00", "2022-10-01T00:00:00",
    #                "2022-11-01T00:00:00", "2022-12-01T00:00:00"]}

if __name__ == "__main__":
    test_aggregate(collection)

