# common/__init__.py

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
        path="/common/static",
        app=staticfiles.StaticFiles(directory="app/common/static"),
        name="common_static",
    )
    app.mount(
        path="/common/media",
        app=staticfiles.StaticFiles(directory="app/common/media"),
        name="common_media",
    )

    # api
    app.include_router( router )