from sqlalchemy import Column, Integer, String, DateTime, func, Float, Boolean
from db import Base
from sqlalchemy import ForeignKey

class MangaGenre(Base):
    __tablename__ = "manga_genres"

    manga_id = Column(Integer, ForeignKey("manga.id"), primary_key=True)
    genre_name = Column(String, ForeignKey("genres.name"), primary_key=True)    