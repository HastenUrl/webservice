from fastapi import FastAPI

from .routes import users, urls

app = FastAPI()

app.include_router(users.router)
app.include_router(urls.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}