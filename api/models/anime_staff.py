from sqlalchemy import Column, Integer, String, DateTime, func, Float, Boolean
from db import Base
from sqlalchemy import ForeignKey


class AnimeStaff(Base):
    __tablename__ = "anime_staff"

    anime_id = Column(Integer, ForeignKey("anime.id"), primary_key=True)
    staff_id = Column(Integer, ForeignKey("staff.id"), primary_key=True)
    role = Column(String)
