# post/api.py

# lib
from fastapi import Depends, Query
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import Response, JSONResponse, RedirectResponse, FileResponse

# module

# define
router = APIRouter()

template = Jinja2Templates(directory="template")


@router.get("/")
async def get_root(req:Request):
    resp = template.TemplateResponse(
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
    return FileResponse("static/image/favicon.ico")

