from sqlalchemy import Column, Integer, String, DateTime, func, Float, Boolean
from db import Base

class Tag(Base):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    category = Column(String)
    is_spoiler = Column(Boolean)
    is_adult = Column(Boolean)
