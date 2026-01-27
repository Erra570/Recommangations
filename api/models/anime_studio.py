from sqlalchemy import Column, Integer, String, DateTime, func, Float, Boolean
from db import Base
from sqlalchemy import ForeignKey


class AnimeStudio(Base):
    __tablename__ = "anime_studio"

    anime_id = Column(Integer, ForeignKey("anime.id"), primary_key=True)
    studio_id = Column(Integer, ForeignKey("studio.id"), primary_key=True)
