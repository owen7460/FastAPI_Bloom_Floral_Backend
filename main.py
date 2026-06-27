from contextlib import asynccontextmanager
from datetime import datetime
from decimal import Decimal

from fastapi import FastAPI, Depends
from sqlalchemy import DateTime, func, String, Text, Numeric, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

ASYNC_DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/fastapi_bloom_floral_backend?charset=utf8mb4"

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
    __tablename__ = "flowers"

    id:Mapped[int] = mapped_column(primary_key=True, comment="flower ID")
    name:Mapped[str] = mapped_column(String(255),comment="flower Name")
    price: Mapped[Decimal] = mapped_column(Numeric(10,2),comment= "flower Price")
    description: Mapped[str] = mapped_column(Text, nullable=True, comment="flower Description")
    stock: Mapped[int] = mapped_column(default=0, comment="flower number")
    image_url:Mapped[str] = mapped_column(String(255),comment="pictures url")
    is_active:Mapped[bool] = mapped_column(default=True, comment="flower Available")

async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def lifespan(app:FastAPI):
    await create_tables()
    yield
    await async_engine.dispose()
app = FastAPI(lifespan=lifespan)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_database():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


@app.get("/")
async def root():
    return {"message": "Hello, this is backend for florist -- Bloom Floral!"}

@app.get("/flowers")
async def get_flowers(db:AsyncSession = Depends(get_database)):
    result = await db.execute(select(Flower))
    flowers = result.scalars().all()
    return {
        "code": 200,
        "msg": "success",
        "flowers": flowers
    }

