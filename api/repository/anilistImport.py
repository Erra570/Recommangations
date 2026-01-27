from models import *
from db import get_db

def insert_media(media):
    session = get_db()

    for subs in media.values():
        for entry in subs:
            session.add(entry)

    session.commit()
    session.close()