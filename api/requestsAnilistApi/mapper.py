from models import *
import numpy as np

def anime_to_entry(media):
	anime = Anime()
	anime.id					= media["id"]
	anime.cover_image			= media["coverImage"]
	anime.title_romaji			= media["title"]["romaji"]
	anime.title_english			= media["title"]["english"]
	anime.format				= media["format"]
	anime.start_date			= media["startDate"]
	anime.country_of_origin		= media["countryOfOrigin"]
	anime.mean_score			= media["meanScore"]
	anime.dropped_paused		= media["droppedPaused"]
	anime.completed_watching	= media["completedWatching"]
	anime.planning				= media["planning"]
	anime.variance_score		= media["scoreVariance"]
	anime.status				= media["status"]
	anime.favourites			= media["favourites"]
	anime.updated_at			= media["updatedAt"]
	anime.episodes				= media["episodes"]
	anime.is_adult				= media["isAdult"]

	tags = []
	for m_tag in media["tags"]:
		tag = AnimeTag()
		tag.anime_id	= anime.id
		tag.tag_id		= m_tag["id"]
		tag.rank		= m_tag["rank"]
		tag.is_spoiler	= m_tag["isMediaSpoiler"]
		tags.append(tag)
	
	genres = []
	for name_genre in media["genres"]:
		genre = AnimeGenre()
		genre.anime_id		= anime.id
		genre.genre_name	= name_genre
		genres.append(genre)

	studios = []
	for id_studio in media["studios"]:
		studio = AnimeStudio()
		studio.anime_id		= anime.id
		studio.studio_id	= id_studio
		studios.append(studio)

	staffs = []
	for m_staff in media["staffs"]:
		staff = AnimeStaff()
		staff.anime_id	= anime.id
		staff.staff_id	= m_staff["id"]
		staff.role		= m_staff["role"]
		staffs.append(staff)
	
	return {"Anime": [anime],
		 	"AnimeTag": tags,
			"AnimeGenre": genres,
			"AnimeStudio": studios,
			"AnimeStaff": staffs}

def animes_to_entries(medias):
	rep = []
	for media in medias:
		rep.append(anime_to_entry(media))
	
	return rep


def manga_to_entry(media):
	manga = Manga()
	manga.id					= media["id"]
	manga.cover_image			= media["coverImage"]
	manga.title_romaji			= media["title"]["romaji"]
	manga.title_english			= media["title"]["english"]
	manga.format				= media["format"]
	manga.start_date			= media["startDate"]
	manga.country_of_origin		= media["countryOfOrigin"]
	manga.mean_score			= media["meanScore"]
	manga.dropped_paused		= media["droppedPaused"]
	manga.completed_watching	= media["completedWatching"]
	manga.planning				= media["planning"]
	manga.variance_score		= media["scoreVariance"]
	manga.status				= media["status"]
	manga.favourites			= media["favourites"]
	manga.updated_at			= media["updatedAt"]
	manga.chapters				= media["chapters"]
	manga.is_adult				= media["isAdult"]

	tags = []
	for m_tag in media["tags"]:
		tag = MangaTag()
		tag.manga_id	= manga.id
		tag.tag_id		= m_tag["id"]
		tag.rank		= m_tag["rank"]
		tag.is_spoiler	= m_tag["isMediaSpoiler"]
		tags.append(tag)
	
	genres = []
	for name_genre in media["genres"]:
		genre = MangaGenre()
		genre.manga_id		= manga.id
		genre.genre_name	= name_genre
		genres.append(genre)

	staffs = []
	for m_staff in media["staffs"]:
		staff = MangaStaff()
		staff.manga_id	= manga.id
		staff.staff_id	= m_staff["id"]
		staff.role		= m_staff["role"]
		staffs.append(staff)
	
	return {"Manga": [manga],
		 	"MangaTag": tags,
			"MangaGenre": genres,
			"MangaStaff": staffs}

def manga_to_entries(medias):
	rep = []
	for media in medias:
		rep.append(manga_to_entry(media))
	
	return rep

def tag_to_entries(tags):
	rep = []
	for m_tag in tags:
		tag = Tag()
		tag.id			= m_tag["id"]
		tag.category	= m_tag["category"]
		tag.name		= m_tag["name"]
		tag.is_spoiler	= m_tag["isGeneralSpoiler"]
		tag.is_adult	= m_tag["isAdult"]
		rep.append(tag)
	return rep

def genre_to_entries(genre_names):
	rep = []
	for genre_name in genre_names:
		genre = Genre()
		genre.name = genre_name
		rep.append(genre)
	return rep

def staff_to_entries(staffs):
	rep = []
	for m_staff in staffs:
		staff = Staff()
		staff.id = m_staff["id"]
		staff.name = m_staff["name"]["full"]
		rep.append(staff)
	return rep

def studio_to_entries(studios):
	rep = []
	for m_studio in studios:
		studio = Studio()
		studio.id = m_studio["id"]
		studio.name = m_studio["name"]
		rep.append(studio)
	return rep