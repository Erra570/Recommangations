from sqlalchemy import Column, Integer, String, DateTime, func, Float, Boolean
from db import Base
from sqlalchemy import ForeignKey

class MangaGenre(Base):
    __tablename__ = "manga_genre"

    manga_id = Column(Integer, ForeignKey("manga.id"), primary_key=True)
    genre_name = Column(String, ForeignKey("genre.name"), primary_key=True)    