# profile/__init__.py

# lib
from fastapi import FastAPI, staticfiles

# module
from .api import router
from .service import *
from .crud import *
from .model import *
from .schema import *

# define
def setup(app:FastAPI):
    # mount
    app.mount(
        path="/profile/static",
        app=staticfiles.StaticFiles(directory="app/profile/static"),
        name="profile_static"
    )
    app.mount(
        path="/profile/media",
        app=staticfiles.StaticFiles(directory="app/profile/media"),
        name="profile_media"
    )

    # api
    app.include_router( router )