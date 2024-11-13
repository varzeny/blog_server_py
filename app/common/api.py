# post/api.py

# lib
from fastapi import Depends, Query
from fastapi.routing import APIRouter
from fastapi.requests import Request
from fastapi.responses import Response, JSONResponse, RedirectResponse, FileResponse

# module
from app.core.config.template import TEMPLATE

# define
router = APIRouter()



@router.get("/")
async def get_root(req:Request):
    resp = TEMPLATE.TemplateResponse(
        request=req,
        name="root.html",
        context={
            "access_token":req.state.access_token,
            "roles":req.state.access_token.roles
        },
        status_code=200
    )
    return resp


@router.get("/favicon.ico")
async def get_favicorn():
    return FileResponse("app/core/static/image/favicon.ico")

