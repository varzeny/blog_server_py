# post/__init__.py

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
        path="/post/static",
        app=staticfiles.StaticFiles(directory="app/post/static"),
        name="post_static"
    )
    app.mount(
        path="/post/media",
        app=staticfiles.StaticFiles(directory="app/post/media"),
        name="post_media"
    )

    # api
    app.include_router( router )