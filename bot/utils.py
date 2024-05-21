from datetime import datetime, timedelta
import calendar
from models import MessageData

def aggregate(data: MessageData, collection):
    if data.group_type == "day":
        date_format = "%Y-%m-%dT00:00:00"
        date_parts = {"year": "$_id.year", "month": "$_id.month", "day": "$_id.day"}
        group_format = get_day_pipeline()
    elif data.group_type == "hour":
        date_format = "%Y-%m-%dT%H:00:00"
        date_parts = {"year": "$_id.year", "month": "$_id.month",
                      "day": "$_id.day", "hour": "$_id.hour"}
        group_format = get_hour_pipeline()
    else:
        date_format = "%Y-%m-01T00:00:00"
        date_parts = {"year": "$_id.year", "month": "$_id.month"}
        group_format = get_month_pipeline()

    pipeline = [
        {
            "$match": {
                "dt": {"$gte": data.dt_from, "$lte": data.dt_upto}
            }
        },
        group_format[0],
        group_format[1],
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
        out_data = list(collection.aggregate(pipeline))
        output = {
            "dataset": [doc["value"] for doc in out_data],
            "labels": [doc["label"] for doc in out_data]
        }
        return fill_with_zero(output, data)
    except Exception as e:
        print(e)


def get_hour_pipeline():
    return [{
            "$group": {
                "_id": {
                    "year": {"$year": "$dt"},
                    "month": {"$month": "$dt"},
                    "day": {"$dayOfMonth": "$dt"},
                    "hour": {"$hour": "$dt"}
                },
                "total_value": {"$sum": "$value"}
            }
        }, {
            "$sort": {"_id.year": 1, "_id.month": 1, "_id.day": 1, "_id.hour": 1}
        }]


def get_day_pipeline():
    return [{
            "$group": {
                "_id": {
                    "year": {"$year": "$dt"},
                    "month": {"$month": "$dt"},
                    "day": {"$dayOfMonth": "$dt"}
                },
                "total_value": {"$sum": "$value"}
            }
        }, {
            "$sort": {"_id.year": 1, "_id.month": 1, "_id.day": 1}
        }]


def get_month_pipeline():
    return [{
            "$group": {
                "_id": {
                    "year": {"$year": "$dt"},
                    "month": {"$month": "$dt"}
                },
                "total_value": {"$sum": "$value"}
            }
        }, {
            "$sort": {"_id.year": 1, "_id.month": 1}
        }]


def fill_with_zero(data, message_data: MessageData):
    start_date = message_data.dt_from
    end_date = message_data.dt_upto

    new_dataset = []
    new_labels = []

    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%dT%H:%M:%S')
        if date_str in data['labels']:
            index = data['labels'].index(date_str)
            new_dataset.append(data['dataset'][index])
            new_labels.append(date_str)
        else:
            print('detected missing date: ' + date_str)
            new_dataset.append(0)
            new_labels.append(date_str)

        if message_data.group_type == 'hour':
            current_date += timedelta(hours=1)
        elif message_data.group_type == 'day':
            current_date += timedelta(days=1)
        else :
            current_date = add_months(current_date, 1)

    data['dataset'] = new_dataset
    data['labels'] = new_labels

    return data


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.date(year, month, day)