
from bson.objectid import ObjectId
from fastapi import HTTPException


def validateObjectId(id: str):
    try:
        _id = ObjectId(id)
    except Exception:
        print("Invalid Object ID")
        raise HTTPException(status_code=400, detail="Invalid Object ID")
    return _id
