# code to generate the keys for URLs
# modularizing the code to different functions
# cleans the create_url function, and also allows for 
# easy unit testing

import secrets 
import string

# secrets is the standard Python module for gen cryptographically secure random 
# bytes and strings
def create_random_key(length: int = 5) -> str:
    chars = string.ascii_letters + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))