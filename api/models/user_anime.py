from sqlalchemy import Column, Integer, String, DateTime, func, Float, Boolean
from db import Base
from sqlalchemy import ForeignKey

class UserAnime(Base):
    __tablename__ = "user_anime"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    anime_id = Column(Integer, ForeignKey("anime.id"), primary_key=True)

    status = Column(String)
    score = Column(Float)
    progress = Column(Integer)
    favourite = Column(Boolean)
    repeat = Column(Integer)
    last_watched = Column(DateTime, default=func.now())
