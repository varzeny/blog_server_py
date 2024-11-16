# profile/model.py

# lib
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, TIMESTAMP, ForeignKey, Text
from datetime import datetime

# module
from app.core import ORM

# define
class History(ORM.base):
    __tablename__ = "history"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    date: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    summary: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    type:Mapped[str] = mapped_column(String(45), nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date.strftime('%Y-%m-%d %H:%M:%S') if self.date else None,
            "title": self.title,
            "summary": self.summary,
            "content": self.content,
            "type": self.type,
            "url": self.url,
        }


class Project(ORM.base):
    __tablename__="project"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    thumbnail:Mapped[str] = mapped_column(String(255), nullable=True)
    title:Mapped[str] =  mapped_column(String(60), nullable=False, unique=True)
    summary:Mapped[str] = mapped_column(String(255), nullable=False)
    github:Mapped[str] = mapped_column(String(255), nullable=True)

    def to_dict(self):
        return {
            "id":self.id,
            "thumbnail":self.thumbnail,
            "title":self.title,
            "summary":self.summary,
            "github":self.github
        }