# FastAPI implementation that has one endpoint 

from fastapi import FastAPI

# define app by instantiating FastAPI
# the app variable is the main point of interaction to create the API
app = FastAPI()

# path operation decorator associates root path with read_root()
# by registering it with FastAPI
# FastAPI will listen to the root path and delegate all
# incoming GET requests to read_root()
# The string will be displayed when a req is sent to the root path of the API
@app.get("/")
def read_root():
    return "Welcome to URL Shortener app :)"


# to run the app, we need a server 
# $ uvicorn shortener_app.main:app --reload
# check http://127.0.0.1:8000
# use http://127.0.0.1:8000/docs for documentation