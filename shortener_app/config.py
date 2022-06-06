# setting the environment variables

from functools import lru_cache

from pydantic import BaseSettings


# Settings is a subclass of BaseSettings
# BaseSettings used to define env variables - only have to define variables
# you want to use, others are assumed default
class Settings(BaseSettings):
    env_name: str = "Local"
    base_url: str = "http://localhost:8000"
    db_url: str = "sqlite:///./shortener.db"

# Storing external env variables follows 12-factor app methodology
# .env file added to root dir - to load it, following code is added
    class Config:
        env_file = ".env"

# using the lru decorator to cache the results of get_settings 
# this decreases the load on computing resources
@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    print(f"Loading settings for: {settings.env_name}")
    return settings