from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine

app = FastAPI()
ASYNC_DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/FastAPI_Bloom_Floral_Backend?charset=utf8"

async_engine = create_async_engine(
ASYNC_DATABASE_URL,
    echo = True,
    pool_size = 10,
    max_overflow= 20
)



@app.get("/")
async def root():
    return {"message": "Hello, this is backend for florist -- Bloom Floral!"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"{name} Hello from Bloom Floral!"}
