# post/api.py

# lib
import os, aiofiles, math
from typing import Optional
from fastapi import Depends, Query, UploadFile
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import Response, JSONResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, insert, update, func, desc, asc, text

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

    resp = template.TemplateResponse(
        request=req,
        name="post_root.html",
        context={
            "access_token":req.state.access_token,
            "categories":categories,
            "tags":tags,
        },
        status_code=200
    )
    return resp


@router.get("/search")
async def get_search(
    req:Request,
    target:Optional[str] = Query(None, min_length=1, max_length=50),
    id:Optional[str] = Query(None),
    page:int|None = Query(0),
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
                select(Post.id, Post.state, Post.title, Post.thumbnail, Post.summary, Post.account_name, Post.created_at)
                .where(Post.category_id==id)
                .where(Post.state==True)
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
                select(Post.id, Post.state, Post.title, Post.thumbnail, Post.summary, Post.account_name, Post.created_at)
                .join(PostTag, Post.id == PostTag.post_id)
                .where(PostTag.tag_id==id)
                .where(Post.state==True)
                .order_by( desc(Post.updated_at) )
                .offset(page*SETTING["app"]["post"]["pagesize"])
                .limit(SETTING["app"]["post"]["pagesize"])
            )

        else:# 전체:생성일 기준 최근 5개
            respCount = await ss.execute(
                select( func.count() ).select_from(Post).where(Post.state==True)
            )
            count = respCount.scalar()
            pages = math.ceil( count / SETTING["app"]["post"]["pagesize"] )

            resp = await ss.execute( 
                select(Post.id, Post.state, Post.title, Post.thumbnail, Post.summary, Post.account_name, Post.created_at)
                .where(Post.state == True)
                .order_by( desc(Post.created_at) )
                .offset(page*SETTING["app"]["post"]["pagesize"])
                .limit(SETTING["app"]["post"]["pagesize"])
            )


        respDate = [ {key: (value.isoformat() if isinstance(value, datetime) else value) for key, value in r.items()} for r in resp.mappings().fetchall() ]
        print("restData : ",respDate)

        return JSONResponse(content={"post_list":respDate, "pages":pages, "page":page}, status_code=200)
    
    except Exception as e:
        print("ERROR from get_search : ", e)
        return Response(status_code=400)



@router.get("/read/{post_id}")
async def get_detail(req:Request, post_id:int, ss:AsyncSession=Depends(DB.get_ss)):
    print(post_id)

    # db에서 해당 포스트가 있으면
    resp = await ss.execute(
        select(Post).where(Post.id==post_id).where(Post.state==True)
    )
    respData = resp.scalar_one_or_none()
    if not respData:
        print("포스트 가져오기 실패")
        return Response(status_code=400)

    # 조회수 상승
    respData.view += 1
    await ss.commit()

    post = respData.__dict__

    post.pop("_sa_instance_state")
    post["created_at"] = post["created_at"].isoformat()
    print(post)


    # 페이지 반환
    resp = template.TemplateResponse(
        request=req,
        name="post_read.html",
        context={
            "access_token":req.state.access_token,
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
            "access_token":req.state.access_token,
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







# comment
@router.post("/write/comment")
async def post_write_comment(req:Request, at=Depends(user_only), ss:AsyncSession=Depends(DB.get_ss)):
    # 폼내용 받기
    formData = await req.form()

    #db에 넣기
    new_comment = Comment(
        post_id=formData.get("post_id"),
        parent_id=formData.get("parent_id") if formData.get("parent_id") else None, 
        account_id = at.sub,
        account_name = at.name,
        content = formData.get("content"),
    )
    ss.add(new_comment)
    await ss.commit()



@router.get("/read/comment/{post_id}")
async def get_read_comment(req:Request, post_id:int, ss:AsyncSession=Depends(DB.get_ss)):
    # 코맨트 불러오기
    resp = await ss.execute(
        select(Comment)
        .where(Comment.post_id==post_id)
        .order_by( asc(Comment.created_at) )
    )
    respData = resp.scalars().all()
    comments = []
    for c in respData:
        d = c.__dict__
        d.pop("_sa_instance_state")
        d["created_at"] = d["created_at"].isoformat()
        d["updated_at"] = d["updated_at"].isoformat()
        comments.append(d)
    # print(comments)

    return JSONResponse( content={"comments":comments}, status_code=200 )


@router.get("/delete/comment/{comment_id}")
async def get_delete_comment(req:Request, comment_id:int, at=Depends(user_only), ss:AsyncSession=Depends(DB.get_ss)):

    result = await ss.execute(
        select(Comment)
        .where(Comment.id==comment_id)
    )
    comment = result.scalar_one_or_none()

    if at.sub == comment.account_id:
        await ss.delete(comment)
        await ss.commit()
        return Response(status_code=200)
    else:
        return Response(status_code=401)