# code to generate the keys for URLs
# modularizing the code to different functions
# cleans the create_url function, and also allows for 
# easy unit testing

import secrets 
import string

from sqlalchemy.orm import Session
from . import crud

# secrets is the standard Python module for gen cryptographically secure random 
# bytes and strings
def create_random_key(length: int = 5) -> str:
    chars = string.ascii_letters + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))

# creating a unique key, will keep checking if key already 
# exists in the db, returns first available key
def create_unique_random_key(db: Session) -> str:
    key = create_random_key()
    while crud.get_db_url_by_key(db, key):
        key = create_random_key()
    return key
