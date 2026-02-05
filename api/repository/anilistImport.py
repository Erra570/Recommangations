from fastapi import Depends
from models import *
from db import get_db
from sqlalchemy import MetaData


def insert_media(medias):
    for media in medias:
        for entries in media.values():
            add_all(entries)
    return True

def update_media(medias):
    flag = True
    for session in get_db():
        for media in medias:
            if "Anime" in media:
                new_media = media["Anime"][0]
                db_media = session.get(Anime, new_media.id)
            else:
                new_media = media["Manga"][0]
                db_media = session.get(Manga, new_media.id)
            if db_media is None or db_media.updated_at < new_media.updated_at:
                if not db_media is None:
                    session.delete(db_media)
                session.add(new_media)
                for key, entries in media.items():
                    if not key in ["Anime", "Manga"]:
                        add_all(entries)
            else:
                flag = False
    return flag

def add_all(list):
    flag = True
    for session in get_db():
        for entry in list:
            try:
                session.add(entry)
                session.flush()
            except:
                session.rollback()
                flag = False
            else:
                session.commit()
        break
    return flag

def purge_all():
    meta = MetaData()

    for session in get_db():
        for tbl in reversed(meta.sorted_tables):
            session.execute(tbl.delete())
        break
