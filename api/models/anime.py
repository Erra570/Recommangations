from sqlalchemy import Column, Integer, String, DateTime, func, Float, Boolean
from api.db import Base

class Anime(Base):
    __tablename__ = "anime"

    id = Column(Integer, primary_key=True, index=True)
    cover_image = Column(String)

    title_romaji = Column(String)
    title_english = Column(String)
    format = Column(String)
    start_date = Column(DateTime)
    country_of_origin = Column(String)

    mean_score = Column(Float)
    dropped_paused = Column(Integer)
    completed_watching = Column(Integer)
    planning = Column(Integer)
    variance_score = Column(Float)
    status = Column(String)
    favourites = Column(Integer)
    updated_at = Column(Integer)
    episodes = Column(Integer)
    

    is_adult = Column(Boolean, default=False)
