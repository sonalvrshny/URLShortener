# schema is what the API expects as a request body and what 
# client can expect in response body

from pydantic import BaseModel

# target_url stores the URL that the shortened URL forwards to
class URLBase(BaseModel):
    target_url: str

# This class inherits target_url 
# is_active allows to deactivate shortened URLs
# clicks counts how many times a shortened URL is visited
class URL(URLBase):
    is_active: bool
    clicks: int

    # telling pydantic to work with a database model 
    # orm is object relational mapping 
    class Config:
        orm_mode = True

# by adding another class for url and admin_url variables, 
# data can be used in the API without storing in db
class URLInfo(URL):
    url: str
    admin_url: str