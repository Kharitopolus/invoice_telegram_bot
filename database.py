from settings import settings
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(settings.database_url)
async_session_maker = async_sessionmaker(
    engine, expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass
