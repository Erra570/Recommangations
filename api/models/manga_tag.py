from sqlalchemy import Column, Integer, String, DateTime, func, Float, Boolean
from db import Base
from sqlalchemy import ForeignKey

class MangaTag(Base):
    __tablename__ = "manga_tag"

    manga_id = Column(Integer, ForeignKey("manga.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tag.id"), primary_key=True)
    is_spoiler = Column(Boolean)
    rank = Column(Integer)
