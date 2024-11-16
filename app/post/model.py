# post/model.py

# lib
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, Boolean, TIMESTAMP, func, ForeignKey
from datetime import datetime

# module
from app.core import ORM


# define

class Category(ORM.base):
    __tablename__="category"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    
    # 카테고리가 가진 모든 포스트 참조
    posts = relationship("Post", back_populates="category")


class Tag(ORM.base):
    __tablename__="tag"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(45), nullable=False, unique=True)
    
    # 태그가 포함된 포스트 참조 (다대다 관계)
    posts = relationship("Post", secondary="post_tag", back_populates="tags")


class Post(ORM.base):
    __tablename__="post"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id", ondelete="CASCADE", onupdate="CASCADE"))
    state: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    account_id: Mapped[int] = mapped_column(Integer, nullable=False)
    account_name: Mapped[str] = mapped_column(String(45), nullable=False)

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[str] = mapped_column(String(255), default="There is no summary.", nullable=True)
    thumbnail: Mapped[str] = mapped_column(String(255), default="/post/media/thumbnail_default.png", nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    view: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    like: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # 카테고리와의 다대일 관계
    category = relationship("Category", back_populates="posts")

    # 댓글과의 일대다 관계
    comments = relationship("Comment", back_populates="post", cascade="all, delete")

    # 태그와의 다대다 관계 (PostTag 테이블 사용)
    tags = relationship("Tag", secondary="post_tag", back_populates="posts", cascade="all, delete")


class Comment(ORM.base):
    __tablename__="comment"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    parent_id: Mapped[int] = mapped_column(ForeignKey("comment.id", ondelete="CASCADE", onupdate="CASCADE"), default=None, nullable=True)
    account_id: Mapped[int] = mapped_column(Integer, nullable=False)
    account_name: Mapped[str] = mapped_column(String(45), nullable=False)

    content: Mapped[str] = mapped_column(Text, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # 포스트와의 다대일 관계
    post = relationship("Post", back_populates="comments")

    # 자기 참조 관계 설정 (대댓글을 위한 관계)
    parent = relationship("Comment", remote_side=[id], backref="children")


class PostTag(ORM.base):
    __tablename__ = "post_tag"
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tag.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
