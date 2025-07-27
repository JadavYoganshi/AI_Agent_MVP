# from fastapi import FastAPI, HTTPException
# from duckduckgo_search import DDGS

# app = FastAPI(title="Search Service", version="1.0")

# @app.get("/search")
# def search(q: str):
#     try:
#         print(f"Searching for: {q}")
#         with DDGS() as ddgs:
#             # ddgs.text returns a list of dictionaries
#             results = ddgs.text(q, region="wt-wt", safesearch="Off", max_results=1)
            
#             if not results:
#                 raise HTTPException(status_code=404, detail="No results found")
            
#             # Access the first result
#             answer = results[0].get("body", "No result found.")
#             return {"answer": answer}
    
#     except Exception as e:
#         print(f"Search failed: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

from fastapi import FastAPI, HTTPException
from duckduckgo_search import DDGS
import requests
from pydantic import BaseModel

app = FastAPI(title="Search Service", version="1.0")

HISTORY_SERVICE_URL = "http://history_service:8003/add"

class HistoryItem(BaseModel):
    question: str
    answer: str
    source: str

@app.get("/search")
def search(q: str):
    try:
        print(f"Searching for: {q}")
        with DDGS() as ddgs:
            results = ddgs.text(q, region="wt-wt", safesearch="Off", max_results=1)
            answer = next(iter(results), None)
            if answer:
                result_text = answer.get("body", "No result found.")

                # Add to history
                history_payload = {
                    "question": q,
                    "answer": result_text,
                    "source": "search"
                }
                try:
                    res = requests.post(HISTORY_SERVICE_URL, json=history_payload)
                    res.raise_for_status()
                except Exception as history_err:
                    print(f"Failed to save to history: {history_err}")

                return {"answer": result_text}
            else:
                raise HTTPException(status_code=404, detail="No results found")
    except Exception as e:
        print(f"Search failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")
