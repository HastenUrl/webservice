from typing import Annotated
from dotenv import load_dotenv
from fastapi import Depends, FastAPI

from .config.redis import get_redis
from .config.kafka import KafkaConnector, KafkaConsumer

from .routes import users, urls

app = FastAPI()

load_dotenv()

app.include_router(users.router)
app.include_router(urls.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/kafka-test")
def kafka_connection_test():
    kfc = KafkaConnector()
    kc = KafkaConsumer()
    kfc.produce('test', "This is a sample message")

    # consumer = kfc.__get_consumer('123', 'test')

    print("Trial 1")
    kfc.consume('123', 'test')

    # print("Trial 2")
    # kc.consume(consumer)

    # producer = kfc.__get_producer()
    
    return {"message": "Done"}

@app.get("/redis-test")
def redis_connection_test(cache = Depends(get_redis)):
    try:
        cache.set("connection", "stable")
        return {"message": cache.get("connection")}
    except Exception as e:
        return {"message": str(e)}
    return {"message": "Not working"}