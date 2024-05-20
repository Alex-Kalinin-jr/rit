import datetime
from pymongo import MongoClient
from models import MessageData

def aggregate(data: MessageData, collection):
    if data.group_type == "day":
        date_format = "%Y-%m-%dT00:00:00"
        date_parts = {"year": "$_id.year", "month": "$_id.month", "day": "$_id.day"}
    elif data.group_type == "hour":
        date_format = "%Y-%m-%dT%H:00:00"
        date_parts = {"year": "$_id.year", "month": "$_id.month", "day": "$_id.day", "hour": "$_id.hour"}
    else:  # Default to "month"
        date_format = "%Y-%m-01T00:00:00"
        date_parts = {"year": "$_id.year", "month": "$_id.month"}

    pipeline = [
        {
            "$match": {
                "dt": {"$gte": data.dt_from, "$lte": data.dt_upto}
            }
        },
        {
            "$group": {
                "_id": {
                    "year": {"$year": "$dt"},
                    "month": {"$month": "$dt"},
                    "day": {"$dayOfMonth": "$dt"},
                    "hour": {"$hour": "$dt"}
                },
                "total_value": {"$sum": "$value"}
            }
        },
        {
            "$sort": {"_id.year": 1, "_id.month": 1, "_id.day": 1, "_id.hour": 1}
        },
        {
            "$project": {
                "_id": 0,
                "value": "$total_value",
                "label": {
                    "$dateToString": {
                        "format": date_format,
                        "date": {"$dateFromParts": date_parts}
                    }
                }
            }
        }
    ]

    try:
        data = list(collection.aggregate(pipeline))
        output = {
            "dataset": [doc["value"] for doc in data],
            "labels": [doc["label"] for doc in data]
        }
        return summarize_values(output)
    except Exception as e:
        print(e)

def summarize_values(data):
    values = []
    dates = []
    current_sum = data["values"][0]
    current_date = data["labels"][0]

    for i in range(len(data["dataset"])):
        if data["labels"][i] == current_date:
            current_sum += data["dataset"][i]
        else:
            values.append(current_sum)
            dates.append(current_date)
            current_sum = data["dataset"][i]
            current_date = data["labels"][i]

    # Add the last sum and date
    values.append(current_sum)
    dates.append(current_date)

    return {"dataset": values, "labels": dates}

