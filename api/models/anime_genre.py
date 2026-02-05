from sqlalchemy import Column, Integer, String, DateTime, func, Float, Boolean
from db import Base
from sqlalchemy import ForeignKey

class AnimeGenre(Base):
    __tablename__ = "anime_genre"

    anime_id = Column(Integer, ForeignKey("anime.id"), primary_key=True)
    genre_name = Column(String, ForeignKey("genre.name"), primary_key=True)