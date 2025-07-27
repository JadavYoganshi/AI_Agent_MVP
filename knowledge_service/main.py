from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List

app = FastAPI(title="Knowledge Base Service", version="1.0")

# Simple in-memory knowledge store
store: Dict[str, str] = {}

# Request model
class KnowledgeItem(BaseModel):
    question: str
    answer: str

@app.post("/add")
def add_knowledge(item: KnowledgeItem):
    store[item.question.lower()] = item.answer
    return {"message": "Knowledge added successfully."}

@app.post("/bulk-add")
def bulk_add(items: List[KnowledgeItem]):
    for item in items:
        store[item.question.lower()] = item.answer
    return {"message": f"{len(items)} knowledge items added."}

@app.get("/get")
def get_knowledge(q: str):
    answer = store.get(q.lower())
    if answer:
        return {"answer": answer}
    raise HTTPException(status_code=404, detail="Knowledge not found")
