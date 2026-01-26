from sqlalchemy import Column, Integer, String, DateTime, func
from api.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, unique=True, nullable=False, index=True)
    username = Column(String, unique=True, nullable=False)