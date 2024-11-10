# profile/api.py

# lib
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import Response, JSONResponse, RedirectResponse

# module


# define
router = APIRouter(
    prefix="/profile"
)

template = Jinja2Templates(directory="template")


@router.get("/")
async def get_root(req:Request):
    resp = template.TemplateResponse(
        request=req,
        name="profile.html",
        context={},
        status_code=200
    )

    return resp