from sqlalchemy import Column, Integer, String, DateTime, func, Float, Boolean
from db import Base
from sqlalchemy import ForeignKey

class AnimeTag(Base):
    __tablename__ = "anime_tag"

    anime_id = Column(Integer, ForeignKey("anime.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tag.id"), primary_key=True)
    is_spoiler = Column(Boolean)
    rank = Column(Integer)
