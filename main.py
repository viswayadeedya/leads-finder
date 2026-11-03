from fastapi import FastAPI, HTTPException
import httpx
import logging
from settings import settings
from search import search

app = FastAPI()
logging.basicConfig(
    filename="search.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )
logger = logging.getLogger(__name__)



@app.get("/places")
def place(local_business, city, state):
    try:
        profiles = search(local_business, city, state, 10)
        logger.info(local_business + ' in ' + city+ ', '+ state + ' search success')
        return profiles
    except httpx.HTTPStatusError as e:
        logger.error(e.response.json())
        raise HTTPException(status_code=e.response.status_code, detail=e.response.json())