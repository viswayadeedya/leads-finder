from fastapi import Depends, FastAPI, HTTPException
import httpx
import logging
from load_service import load_profile
from db import get_db
from settings import settings
from search import search
from sqlalchemy.orm import Session

app = FastAPI()

logging.basicConfig(
    filename="search.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )
logger = logging.getLogger(__name__)



@app.get("/places")
def place(local_business, city, state, db: Session = Depends(get_db)):
    try:
        profiles = search(local_business, city, state, 10)
        load_profile(db, local_business, city, state, profiles)
        logger.info(local_business + ' in ' + city+ ', '+ state + ' search success')
        return profiles
    except httpx.HTTPStatusError as e:
        logger.error(e.response.json())
        raise HTTPException(status_code=e.response.status_code, detail=e.response.json())