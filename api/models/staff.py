from sqlalchemy import Column, Integer, String, DateTime, func, Float, Boolean
from api.db import Base

class Staff(Base):
    __tablename__ = "staff"

    id = Column(Integer, primary_key=True)
    name = Column(String)