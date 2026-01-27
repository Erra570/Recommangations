from sqlalchemy import Column, Integer, String, DateTime, func, Float, Boolean
from db import Base

class Studio(Base):
    __tablename__ = "studio"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
