# URL Shortener

In this project, I have created an API to create and manage shortened URLs. The API receives a full target URL and returns a shortened one.

## Objective

Fully functional API-driven web app that creates shortened URLs that forward to target URLs

## Tools and tech

- Python 3.8.10
- FastAPI used to create REST API
- Development server ran with Uvicorn
- SQLite database

## How to use

- Post target URL to URLShortener app
- Receive a shortened URL and secret key back
- Shortened URL contains a random key that forwards to target URL
- Secret key can be used to see stats and delete forwarding
