# orm

# lib
import asyncio
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

# module
from .asyncmy import DB

# define
class Base(AsyncAttrs, DeclarativeBase):
    pass

class Manager:
    base = Base

    @classmethod
    async def setup(cls):
        return

    @classmethod
    async def create_tables(cls):
        async with DB.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)




ORM = Manager()
print("ORM 생성됨")
