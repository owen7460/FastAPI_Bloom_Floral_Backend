from datetime import datetime

from fastapi import FastAPI
from sqlalchemy import DateTime, func
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

app = FastAPI()
ASYNC_DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/FastAPI_Bloom_Floral_Backend?charset=utf8"

async_engine = create_async_engine(
ASYNC_DATABASE_URL,
    echo = True,
    pool_size = 10,
    max_overflow= 20
)

class Base(DeclarativeBase):
    create_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), comment='create_time')
    update_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now() ,comment='update_time')

class Flower(Base):
    pass


@app.get("/")
async def root():
    return {"message": "Hello, this is backend for florist -- Bloom Floral!"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"{name} Hello from Bloom Floral!"}
