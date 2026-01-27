from sqlalchemy import Column, Integer, String, DateTime, func, Float, Boolean
from api.db import Base
from sqlalchemy import ForeignKey


class MangaStaff(Base):
    __tablename__ = "manga_staff"

    manga_id = Column(Integer, ForeignKey("manga.id"), primary_key=True)
    staff_id = Column(Integer, ForeignKey("staff.id"), primary_key=True)
    role = Column(String)
