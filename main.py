from typing import Annotated
from dotenv import load_dotenv
from fastapi import Depends, FastAPI

from .config.redis import get_redis

from .routes import users, urls

app = FastAPI()

load_dotenv()

app.include_router(users.router)
app.include_router(urls.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/redis-test")
def redis_connection_test(cache = Depends(get_redis)):
    try:
        cache.set("connection", "stable")
        return {"message": cache.get("connection")}
    except Exception as e:
        return {"message": str(e)}
    return {"message": "Not working"}