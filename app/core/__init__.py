# core/__init__.py

# lib
from fastapi import FastAPI, staticfiles

# module
from .config.setting import SETTING
from .config.template import TEMPLATE
from .database.asyncmy import DB
from .database.orm import ORM
from .middleware.check_access_token import CheckAccessToken
from .security.dependency import admin_only, user_only, guest_only
from .security.token.access_token import AccessToken


# define
def setup(app:FastAPI):
    # mount
    app.mount(
        path="/core/static",
        app=staticfiles.StaticFiles(directory="app/core/static"),
        name="core_static"
    )
    app.mount(
        path="/core/media",
        app=staticfiles.StaticFiles(directory="app/core/media"),
        name="core_media"
    )

    # middleware
    app.add_middleware( CheckAccessToken )