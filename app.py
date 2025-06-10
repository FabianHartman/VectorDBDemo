from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import chromadb
import requests

class QueryRequest(BaseModel):
    query: str
    n_results: int = 0

app = FastAPI()

chroma_client = chromadb.PersistentClient(path="./chroma_db_step_3")
collection = chroma_client.get_or_create_collection(name="my_collection")

def get_ollama_embeddings(texts, model="mxbai-embed-large"):
    url = "http://localhost:3304/api/embeddings"
    embeddings = []
    for text in texts:
        response = requests.post(url, json={"model": model, "prompt": text})
        response.raise_for_status()
        embedding = response.json()["embedding"]
        embeddings.append(embedding)
    return embeddings

@app.post("/query")
def query_collection(request_data: QueryRequest):
    try:
        query_embedding = get_ollama_embeddings([request_data.query])[0]

        if request_data.n_results != 0:
            results = collection.query(query_embeddings=[query_embedding], n_results=request_data.n_results)
        else:
            results = collection.query(query_embeddings=[query_embedding])

        print(results)
        return {"results": results["documents"][0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))