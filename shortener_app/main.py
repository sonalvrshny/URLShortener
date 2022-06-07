# FastAPI implementation that has one endpoint 

from curses.ascii import HT
import validators
from fastapi import FastAPI, HTTPException

from . import schemas

# define app by instantiating FastAPI
# the app variable is the main point of interaction to create the API
app = FastAPI()

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
@app.post("/url")
def create_url(url: schemas.URLBase):
    if not validators.url(url.target_url):
        raise_bad_request("Your provided URL is not valid")
    return f"TODO:Create database entry for: {url.target_url}"

# to run the app, we need a server 
# $ uvicorn shortener_app.main:app --reload
# check http://127.0.0.1:8000
# use http://127.0.0.1:8000/docs for documentation