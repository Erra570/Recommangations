from sqlalchemy import Column, Integer, String, DateTime, func, Float, Boolean
from api.db import Base
from sqlalchemy import ForeignKey

class MangaGenre(Base):
    __tablename__ = "manga_genres"

    manga_id = Column(Integer, ForeignKey("manga.id"), primary_key=True)
    genre_id = Column(Integer, ForeignKey("genres.id"), primary_key=True)
    