from datetime import datetime

from bson import ObjectId


# used
def to_ObjectId(input_id: str) -> ObjectId:
    return ObjectId(input_id)


def json_serializer(data):
    if isinstance(data, ObjectId):
        return str(data)
    elif isinstance(data, datetime):
        return data.isoformat()
    elif isinstance(data, dict):
        return {k: json_serializer(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [json_serializer(i) for i in data]
    else:
        return data
