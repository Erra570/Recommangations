from sqlalchemy import Column, Integer, String, DateTime, func, Float, Boolean
from db import Base

class Genre(Base):
    __tablename__ = "genres"

    name = Column(String, primary_key=True)