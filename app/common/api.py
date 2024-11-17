# common/api.py

# lib
from fastapi import Depends, Query
from fastapi.routing import APIRouter
from fastapi.requests import Request
from fastapi.responses import Response, JSONResponse, RedirectResponse, FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

# module
from app.core import TEMPLATE
from app.core import DB
from app.post import Post

# define
router = APIRouter()



@router.get("/")
async def get_root(req:Request, ss:AsyncSession=Depends(DB.get_ss)):

    result = await ss.execute(
        select(Post).order_by( desc(Post.view) ).limit(3)
    )
    top3 = result.scalars().all()

    resp = TEMPLATE.TemplateResponse(
        request=req,
        name="root.html",
        context={
            "access_token":req.state.access_token,
            "top3":top3
        },
        status_code=200
    )
    return resp


@router.get("/favicon.ico")
async def get_favicorn():
    return FileResponse("app/core/static/image/favicon.ico")

