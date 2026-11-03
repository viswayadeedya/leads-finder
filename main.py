from fastapi import FastAPI
from settings import settings

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}
