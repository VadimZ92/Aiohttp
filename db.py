from sqlalchemy import Column, String, Integer, DateTime, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from aiohttp import web
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


PG_DSN = "postgresql+asyncpg://app:1234@127.0.0.1:5431/app"
engine = create_async_engine(PG_DSN)
Session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()


class Advertising(Base):

    __tablename__ = "app_advertising"

    id = Column(Integer, primary_key=True, autoincrement=True)
    header = Column(String, nullable=False, unique=True)
    description = Column(String)
    creation_time = Column(DateTime, server_default=func.now())
    user = Column(String, nullable=False, index=True)

