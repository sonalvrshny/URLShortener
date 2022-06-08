# FastAPI implementation that has one endpoint 

import secrets
import validators
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import models, schemas
from .database import SessionLocal, engine

# define app by instantiating FastAPI
# the app variable is the main point of interaction to create the API
app = FastAPI()

# binds the database engine
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)

# path operation decorator associates root path with read_root()
# by registering it with FastAPI
# FastAPI will listen to the root path and delegate all
# incoming GET requests to read_root()
# The string will be displayed when a req is sent to the root path of the API
@app.get("/")
def read_root():
    return "Welcome to URL Shortener app :)"

# create_url endpoint expects a URL string as POST request 
@app.post("/url", response_model=schemas.URLInfo)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    if not validators.url(url.target_url):
        raise_bad_request("Your provided URL is not valid")

    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key = "".join(secrets.choice(chars) for _ in range(5))
    secret_key = "".join(secrets.choice(chars) for _ in range(8))
    db_url = models.URL(
        target_url=url.target_url, key=key, secret_key=secret_key
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    db_url.url = key
    db_url.admin_url = secret_key
    return db_url

# to run the app, we need a server 
# $ uvicorn shortener_app.main:app --reload
# check http://127.0.0.1:8000
# use http://127.0.0.1:8000/docs for documentation