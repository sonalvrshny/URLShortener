# FastAPI implementation that has one endpoint 

import validators
from starlette.datastructures import URL
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from . import models, schemas, keygen, crud
from .database import SessionLocal, engine
from .config import get_settings

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

def raise_not_found(request):
    message = f"URL '{request.url}' does not exist"
    raise HTTPException(status_code=404, detail=message)

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

    # chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    # key = "".join(secrets.choice(chars) for _ in range(5))
    # secret_key = "".join(secrets.choice(chars) for _ in range(8))
    db_url = crud.create_db_url(db=db, url=url)

    return get_admin_info(db_url)

# can GET requests from URL provided as argument
@app.get("/{url_key}")
def forward_to_target_url(url_key: str, request: Request, db: Session = Depends(get_db)):
    # := is a walrus op - assigns variables in middle of expressions
    if db_url := crud.get_db_url_by_key(db=db, url_key=url_key):
        crud.update_db_clicks(db=db, db_url=db_url)
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)

# GET URL info using admin secret key
@app.get("/admin/{secret_key}", name="administration info", response_model=schemas.URLInfo,)
def get_url_info(
    secret_key: str, request: Request, db: Session = Depends(get_db)
):
    if db_url := crud.get_db_url_by_secret_key(db, secret_key=secret_key):
        return get_admin_info(db_url)
    else:
        raise_not_found(request)

def get_admin_info(db_url: models.URL) -> schemas.URLInfo:
    base_url = URL(get_settings().base_url)
    admin_endpoint = app.url_path_for(
        "administration info", secret_key=db_url.secret_key
    )
    db_url.url = str(base_url.replace(path=db_url.key))
    db_url.admin_url = str(base_url.replace(path=admin_endpoint))
    return db_url

@app.delete("/admin/{secret_key}")
def delete_url(
    secret_key: str, request: Request, db: Session = Depends(get_db)
):
    if db_url := crud.deactivate_db_url_by_secret_key(db, secret_key=secret_key):
        message = f"Successfully deleted shortened URL for '{db_url.target_url}'"
        return {"detail": message}
    else:
        raise_not_found(request)

# to run the app, we need a server 
# $ uvicorn shortener_app.main:app --reload
# check http://127.0.0.1:8000
# use http://127.0.0.1:8000/docs for documentation