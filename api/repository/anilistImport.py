from models import *
from db import get_db
from sqlalchemy import MetaData, select

def get_anime_short(id: int):
	for session in get_db():
		anime = session.get(Anime, id)
		rep = {}
		rep["title"] = anime.title_english if not (anime.title_english is None or anime.title_english == "") else anime.title_romaji
		rep["cover_image"] = anime.cover_image
		return rep

def get_anime(id:int):
	for session in get_db():
		anime = session.get(Anime, id).__dict__

		anime["genres"] = []
		stmt = select(AnimeGenre).where(AnimeGenre.anime_id == id)
		for row in session.execute(stmt):
			anime["genres"].append(row[0].genre_name)

		anime["tags"] = []
		stmt = select(AnimeTag).where(AnimeTag.anime_id == id)
		for row in session.execute(stmt):
			tag = session.get(Tag, row[0].tag_id).__dict__
			tag["is_specific_spoiler"] = row[0].is_spoiler
			tag["rank"] = row[0].rank
			anime["tags"].append(tag)

		anime["staffs"] = []
		stmt = select(AnimeStaff).where(AnimeStaff.anime_id == id)
		for row in session.execute(stmt):
			staff = session.get(Staff, row[0].staff_id).__dict__
			staff["role"] = row[0].role
			anime["staffs"].append(staff)

		anime["studios"] = []
		stmt = select(AnimeStudio).where(AnimeStudio.anime_id == id)
		for row in session.execute(stmt):
			anime["studios"].append(session.get(Studio, row[0].studio_id).__dict__)

		return anime


def get_manga_short(id: int):
	for session in get_db():
		manga = session.get(Manga, id)
		rep = {}
		rep["title"] = manga.title_english if not (manga.title_english is None or manga.title_english == "") else manga.title_romaji
		rep["cover_image"] = manga.cover_image
		return rep
	
def get_manga(id: int):
	for session in get_db():
		manga = session.get(Manga, id).__dict__

		manga["genres"] = []
		stmt = select(MangaGenre).where(MangaGenre.manga_id == id)
		for row in session.execute(stmt):
			manga["genres"].append(row[0].genre_name)

		manga["tags"] = []
		stmt = select(MangaTag).where(MangaTag.manga_id == id)
		for row in session.execute(stmt):
			tag = session.get(Tag, row[0].tag_id).__dict__
			tag["is_specific_spoiler"] = row[0].is_spoiler
			tag["rank"] = row[0].rank
			manga["tags"].append(tag)

		manga["staffs"] = []
		stmt = select(MangaStaff).where(MangaStaff.manga_id == id)
		for row in session.execute(stmt):
			staff = session.get(Staff, row[0].staff_id).__dict__
			staff["role"] = row[0].role
			manga["staffs"].append(staff)

		return manga



def insert_media(medias):
	for media in medias:
		if "Anime" in media:
			new_media = media["Anime"]
		elif "Manga" in media:
			new_media = media["Manga"]
		elif "User" in media:
			new_media = media["User"]
			print(new_media[0].id)
		add_all(new_media)

		for key, entries in media.items():
			if not key in ["Anime", "Manga", "User"]:
				add_all(entries)
	return True

def update_media(medias):
	flag = True
	for session in get_db():
		for media in medias:
			if "Anime" in media:
				new_media = media["Anime"][0]
				db_media = session.get(Anime, new_media.id)
			elif "Manga" in media:
				new_media = media["Manga"][0]
				db_media = session.get(Manga, new_media.id)
			else:
				break
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
