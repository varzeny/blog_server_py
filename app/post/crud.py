#

# lib
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

# module

# define

## category
async def create_category(name:str, ss:AsyncSession):
    resp = await ss.execute(
        statement=text("INSERT INTO category(name) VALUES(:name)"),
        params={"name":name}
    )
    await ss.commit()
    return


async def read_category(ss:AsyncSession):
    resp = await ss.execute(
        statement=text("SELECT id, name FROM category"),
        params={}
    )
    respData = resp.mappings().fetchall()
    return respData


## tag
async def create_tag(name:str, ss:AsyncSession):
    resp = await ss.execute(
        statement=text("INSERT INTO tag(name) VALUES(:name)"),
        params={"name":name}
    )
    await ss.commit()
    return


async def read_tag(ss:AsyncSession):
    resp = await ss.execute(
        statement=text("SELECT id, name FROM tag"),
        params={}
    )
    respData = resp.mappings().fetchall()
    return respData


# post
async def create_post(post:dict, ss:AsyncSession):

    return