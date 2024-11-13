# profile/api.py

# lib
from fastapi.routing import APIRouter
from fastapi.requests import Request
from fastapi.responses import Response, JSONResponse, RedirectResponse

# module
from app.core.config.template import TEMPLATE

# define
router = APIRouter(
    prefix="/profile"
)



@router.get("/")
async def get_root(req:Request):
    resp = TEMPLATE.TemplateResponse(
        request=req,
        name="profile_root.html",
        context={},
        status_code=200
    )
    return resp


@router.get("/history")
async def get_root(req:Request):
    resp = TEMPLATE.TemplateResponse(
        request=req,
        name="profile_history.html",
        context={},
        status_code=200
    )
    return resp










@router.get("/test")
async def get_root(req:Request):
    resp = TEMPLATE.TemplateResponse(
        request=req,
        name="test.html",
        context={},
        status_code=200
    )
    return resp
