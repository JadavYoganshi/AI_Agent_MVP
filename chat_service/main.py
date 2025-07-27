from fastapi import FastAPI 
import requests
from pydantic import BaseModel

app = FastAPI(title="Chat Service", version="1.0")

class Question(BaseModel):
    query: str

@app.post("/ask")
def ask(question: Question):
    q = question.query
    print(f"Received question: {q}")

    # Step 1: Try knowledge service
    try:
        print("Trying knowledge_service...")
        res = requests.get(f"http://knowledge_service:8001/get", params={"q": q})
        print(f"Knowledge response: {res.status_code}")
        if res.status_code == 200:
            answer = res.json()['answer']
            source = "knowledge"
        else:
            raise Exception("Knowledge service failed.")
    except Exception as e:
        print(f"Knowledge failed: {e}")
        # Step 2: Fallback to search
        try:
            print("Trying search_service...")
            res = requests.get(f"http://search_service:8002/search", params={"q": q})
            print(f"Search response: {res.status_code}")
            answer = res.json()['answer']
            source = "search"
        except Exception as e:
            print(f"Search failed: {e}")
            return {"error": "Both knowledge and search failed."}

    # Step 3: Store in history
    try:
        print("Sending to history_service...")
        requests.post(f"http://history_service:8003/add", json={
            "question": q,
            "answer": answer,
            "source": source
        })
    except Exception as e:
        print(f"History failed: {e}")

    return {"answer": answer, "source": source}

@app.get("/chat")
def chat(message: str):
    question = Question(query=message)
    return ask(question)
