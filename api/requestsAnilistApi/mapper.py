from models import *
import numpy as np

def to_anime_entry(media):
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
	for name_genre in media["genre"]:
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
	
	return {"Anime": np.array([anime]),
			"AnimeTag": np.array(tags),
			"AnimeGenre": np.array(genres),
			"AnimeStudio": np.array(studios),
			"AnimeStaff": np.array(staffs)}

def to_animes_entries(medias):
	rep = {"Anime": np.array(),
		 	"AnimeTag": np.array(),
			"AnimeGenre": np.array(),
			"AnimeStudio": np.array(),
			"AnimeStaff": np.array()}
	
	for media in medias:
		tmp = to_anime_entry(media)
		rep["Anime"] = np.concatenate((rep["Anime"], tmp["Anime"]))
	
	return rep