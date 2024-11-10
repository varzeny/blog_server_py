# post/api.py

# lib
import os, aiofiles, math
from fastapi import Depends, Query, UploadFile
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import Response, JSONResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, insert, update, func, desc

# module
from app.core.config import SETTING
from app.core.security.dependency import guest_only, user_only, admin_only
from app.core.database.asyncmy import DB
from app.post import crud as CRUD
from .model import *
from .service import *

# define
router = APIRouter(
    prefix="/post"
)

template = Jinja2Templates(directory="template")


@router.get("/")
async def get_root(req:Request, ss:AsyncSession=Depends(DB.get_ss)):
    # 사이드바
    categories = await CRUD.read_category(ss)

    tags = await CRUD.read_tag(ss)

    # post list
    resp = await ss.execute( 
        select(Post.state, Post.title, Post.thumbnail, Post.summary, Post.account_name, Post.created_at).where(Post.state==True)
    )
    respData = resp.mappings().fetchall()
    print(respData)

    for p in respData:
        print( p )

    resp = template.TemplateResponse(
        request=req,
        name="post_root.html",
        context={
            "roles":req.state.access_token.roles,
            "categories":categories,
            "tags":tags,
            "post_list":respData,
        },
        status_code=200
    )
    return resp



@router.get("/search")
async def get_search(
    req:Request,
    target:str = Query(..., min_length=1, max_length=50),
    id:int = Query(...),
    page:int = Query(...),
    ss:AsyncSession=Depends(DB.get_ss)
):
    try:
        print("taret : ", target, "id : ", id, "page : ", page)



        if target == "category":
            respCount = await ss.execute(
                select( func.count() ).select_from(Post).where(Post.category_id==id)
            )
            count = respCount.scalar()
            pages = math.ceil( count / SETTING["app"]["post"]["pagesize"] )

            resp = await ss.execute( 
                select(Post.state, Post.title, Post.thumbnail, Post.summary, Post.account_name, Post.created_at)
                .join(PostTag, Post.id == PostTag.post_id)
                .where(PostTag.tag_id==id)
                .order_by( desc(Post.updated_at) )
                .offset(page*SETTING["app"]["post"]["pagesize"])
                .limit(SETTING["app"]["post"]["pagesize"])
            )

        elif target == "tag":
            respCount = await ss.execute(
                select( func.count() ).select_from(PostTag).where(PostTag.tag_id==id)
            )
            count = respCount.scalar()
            pages = math.ceil( count / SETTING["app"]["post"]["pagesize"] )

            resp = await ss.execute( 
                select(Post.state, Post.title, Post.thumbnail, Post.summary, Post.account_name, Post.created_at)
                .join(PostTag, Post.id == PostTag.post_id)
                .where(PostTag.tag_id==id)
                .order_by( desc(Post.updated_at) )
                .offset(page*SETTING["app"]["post"]["pagesize"])
                .limit(SETTING["app"]["post"]["pagesize"])
            )

        else:# 전체:생성일 기준 최근 5개
            print("타겟 없음")

        respDate = [ {key: (value.isoformat() if isinstance(value, datetime) else value) for key, value in r.items()} for r in resp.mappings().fetchall() ]
        print("restData : ",respDate)

        return JSONResponse(content={"post_list":respDate, "pages":pages, "page":page}, status_code=200)
    
    except Exception as e:
        print("ERROR from get_search : ", e)
        return Response(status_code=400)



@router.get("/read/{post_id}")
async def get_detail(req:Request, post_id:int):
    print(post_id)

    # db에서 해당 포스트가 있으면
    post = None

    # 페이지 반환
    resp = template.TemplateResponse(
        request=req,
        name="post_read.html",
        context={
            "post":post
        },
        status_code=200
    )
    return resp



@router.get("/write")
async def get_write(req:Request, at=Depends(admin_only), ss=Depends(DB.get_ss)):

    categories = await CRUD.read_category(ss)

    tags = await CRUD.read_tag(ss)

    resp = template.TemplateResponse(
        request=req,
        name="post_write.html",
        context={
            "categories":categories,
            "tags":tags
        },
        status_code=200
    )
    return resp





@router.post("/write/category")
async def post_write_category(req:Request, at=Depends(admin_only), ss=Depends(DB.get_ss)):
    formData = await req.form()
    await CRUD.create_category(formData.get("name"), ss)
    return Response(status_code=200)


@router.post("/write/tag")
async def post_write_tag(req:Request, at=Depends(admin_only), ss=Depends(DB.get_ss)):
    formData = await req.form()
    await CRUD.create_tag(formData.get("name"), ss)
    return Response(status_code=200)



@router.post("/write/post")
async def post_write_post(req:Request, at=Depends(admin_only), ss=Depends(DB.get_ss)):
    formData = await req.form()
    print(formData)

    today = datetime.today().strftime('%Y/%m/%d')
    media_dir_path = os.path.join( "media", "post" )
    post_dir_path = os.path.join(media_dir_path, today)

    # 저장할게 있는지? ex)썸네일, 첨부파일, 이미지 등 ###############################
    ## thumbnail
    thumbnail = formData.get("thumbnail")
    thumbnail_path = os.path.join( media_dir_path, "thumbnail_default.png" )
    if thumbnail and thumbnail.filename:
        os.makedirs(post_dir_path, exist_ok=True)
        thumbnail_path = os.path.join( post_dir_path, thumbnail.filename )
        async with aiofiles.open(thumbnail_path, "wb") as f:
            await f.write(await thumbnail.read())

    ## etc

    #######################################################################

    new_post = Post(
        category_id = formData.get("category"),
        state = int(formData.get("state")),

        account_id = at.sub,
        account_name = at.name,

        title = formData.get("title"),
        summary = formData.get("summary"),
        thumbnail = thumbnail_path,
        content = formData.get("content"),
    )

    ss.add(new_post)
    await ss.commit()
    await ss.refresh(new_post)

    tags=formData.getlist("tags")
    if tags:
        print(tags)
        for t_id in tags:
            new_pt = PostTag(post_id=new_post.id, tag_id=t_id)
            ss.add( new_pt )
            print(f"포스트:{new_post.id}, 태그:{t_id}")
        await ss.commit()

    return Response(status_code=200)
