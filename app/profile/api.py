# profile/api.py

# lib
import os, aiofiles
from fastapi import Depends, File, UploadFile
from fastapi.routing import APIRouter
from fastapi.requests import Request
from fastapi.responses import Response, JSONResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, asc
from datetime import datetime

# module
from app.core.config.template import TEMPLATE
from app.core.database.asyncmy import DB
from app.core.security.dependency import admin_only, user_only, guest_only
from app.core.security.token.access_token import AccessToken
from .model import *

# define
router = APIRouter(
    prefix="/profile"
)



@router.get("/write")
async def get_write(req:Request):
    resp = TEMPLATE.TemplateResponse(
        request=req,
        name="profile_write.html",
        context={},
        status_code=200
    )
    return resp


@router.post("/write/history")
async def post_write(req:Request, at=Depends(admin_only), ss:AsyncSession=Depends(DB.get_ss)):
    reqData = await req.form()
    # print(reqData)

    date = datetime.strptime(reqData.get("date"), "%Y-%m-%d")
    date_str = date.strftime('%Y%m%d')

    save_path = os.path.join( "app", "profile", "media", "history", date_str )
    url_path = os.path.join( "profile", "media", "history", date_str )

    evidence = reqData.get("evidence")

    if evidence and evidence.filename:
        os.makedirs(save_path, exist_ok=True)
        evidence_save_path = os.path.join( save_path, evidence.filename )
        evidence_url_path = os.path.join( url_path, evidence.filename )
        async with aiofiles.open(evidence_save_path, "wb") as f:
            await f.write(await evidence.read())
    else:
        print("evidence 없음")
        return Response(status_code=400)


    new_history = History(
        date = date,
        title = reqData.get("title"),
        summary = reqData.get("summary"),
        content = reqData.get("content"),
        type = reqData.get("type"),
        url = evidence_url_path
    )

    ss.add(new_history)
    await ss.commit()

    return Response(status_code=200)



@router.post("/write/project")
async def post_write(req:Request, at=Depends(admin_only), ss:AsyncSession=Depends(DB.get_ss)):
    reqData = await req.form()
    print(reqData)

    title = reqData.get("title")
    thumbnail = reqData.get("thumbnail")
    summary = reqData.get("summary")
    github = reqData.get("github")

    title_path = title.translate( str.maketrans( {' ':'_'} ) )
    save_path = os.path.join( "app", "profile", "media", "project", title_path )
    url_path = os.path.join( "profile", "media", "project", title_path, thumbnail.filename )
    

    os.makedirs(save_path, exist_ok=True)

    if thumbnail:
        async with aiofiles.open( os.path.join(save_path, thumbnail.filename), "wb" ) as f:
            await f.write(await thumbnail.read())
        
    new_project = Project(
        thumbnail = url_path,
        title = title,
        summary = summary,
        github = github
    )

    ss.add(new_project)
    await ss.commit()

    return Response(status_code=200)





@router.get("/")
async def get_root(req:Request):
    resp = TEMPLATE.TemplateResponse(
        request=req,
        name="profile_home.html",
        context={},
        status_code=200
    )
    return resp


@router.get("/history")
async def get_root(req:Request, ss:AsyncSession=Depends(DB.get_ss)):

    resp = await ss.execute( select(History).order_by( desc(History.date) ) )
    respData = resp.scalars().all()


    resp = TEMPLATE.TemplateResponse(
        request=req,
        name="profile_history.html",
        context={"histories":respData},
        status_code=200
    )
    return resp


@router.get("/history/read/{id}")
async def get_read(req:Request, id:int, ss:AsyncSession=Depends(DB.get_ss)):

    query = await ss.execute( select(History).where(History.id==id) )
    queryData = query.scalar()
    print(queryData.to_dict())

    return JSONResponse(content={"history":queryData.to_dict()}, status_code=200)

















@router.get("/experience")
async def get_root(req:Request):
    resp = TEMPLATE.TemplateResponse(
        request=req,
        name="profile_experience.html",
        context={},
        status_code=200
    )
    return resp



@router.get("/project")
async def get_root(req:Request, ss:AsyncSession=Depends(DB.get_ss)):

    resp = await ss.execute( select(Project) )
    respData = resp.scalars().all()
    print(respData)

    resp = TEMPLATE.TemplateResponse(
        request=req,
        name="profile_project.html",
        context={"projects":respData},
        status_code=200
    )
    return resp


