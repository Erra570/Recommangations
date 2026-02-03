import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = os.getenv("DATABASE_URL")

# Car sqlalchemy fait peter les pytests (même si ils ne l'utilise pas encore)
# TODO : trouver ptetre une autre méthode car c'est 2 bâtons et un scotch là
if "pytest" in sys.modules:
    DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
