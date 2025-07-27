from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List

app = FastAPI(title="History Service", version="1.0")
client = MongoClient("mongodb://mongo:27017/")
db = client.history_db
collection = db.records

class HistoryItem(BaseModel):
    question: str
    answer: str
    source: str  # "knowledge" or "search"

@app.post("/add")
def add_record(item: HistoryItem):
    collection.insert_one(item.dict())
    return {"message": "History saved"}

@app.get("/all", response_model=List[HistoryItem])
def get_all():
    return list(collection.find({}, {"_id": 0}))
