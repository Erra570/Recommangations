from sqlalchemy import Column, Integer, String, DateTime, func, Float, Boolean
from db import Base
from sqlalchemy import ForeignKey

class UserManga(Base):
    __tablename__ = "user_manga"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    manga_id = Column(Integer, ForeignKey("manga.id"), primary_key=True)
    
    status = Column(String)
    score = Column(Float)
    progress = Column(Integer)
    favourite = Column(Boolean)
    repeat = Column(Integer)
    last_read = Column(DateTime, default=func.now())