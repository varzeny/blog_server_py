# main.py

# lib

from fastapi import FastAPI, staticfiles

# module
from app import core as CORE
from app import common as COMMON
from app import post as POST
from app import profile as PROFILE

from app.core.middleware.check_access_token import Manager as CheckAccessToken

# define
"""
uvicorn main:app --host 0.0.0.0 --port 9000 --reload

"""

async def startup():
    await CORE.ORM.create_tables()




# app
app = FastAPI()

# event
app.add_event_handler("startup", startup)

# mount
app.mount(
    path="/static",
    app=staticfiles.StaticFiles(directory="static"),
    name="static"
)
app.mount(
    path="/media",
    app=staticfiles.StaticFiles(directory="media"),
    name="media"
)

# middleware
app.add_middleware( CheckAccessToken )

# api
app.include_router( COMMON.api.router )
app.include_router( POST.api.router )
app.include_router( PROFILE.api.router )





