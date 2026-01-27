from sqlalchemy import Column, Integer, String, DateTime, func, Float, Boolean
from api.db import Base
from sqlalchemy import ForeignKey

class AnimeGenre(Base):
    __tablename__ = "anime_genres"

    anime_id = Column(Integer, ForeignKey("anime.id"), primary_key=True)
    genre_id = Column(Integer, ForeignKey("genres.id"), primary_key=True)