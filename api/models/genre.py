from sqlalchemy import Column, Integer, String, DateTime, func, Float, Boolean
from db import Base

class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
