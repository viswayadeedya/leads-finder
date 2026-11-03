from fastapi import FastAPI
from settings import settings
from search import search

app = FastAPI()



@app.get("/places")
def place():
    return search("auto repair", "Lansing", "MI", 10)