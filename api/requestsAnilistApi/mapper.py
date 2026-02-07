from models import *
import numpy as np
import re
from datetime import datetime

def list_processing(list: dict):
    #patern for match staff 
    pattern = re.compile("^(Story|Art|Story & Art|Author|Art & Story|Script|Original Work|Original Story|Original Creator|Director)( .+)*$")

    medias = list["Page"]["media"]
    rm_list = []
    for i, media in enumerate(medias):
        if media["stats"]["scoreDistribution"] == None or media["startDate"]["year"] == None:
            rm_list.append(i)
            #print(media)
        else :
            #date processing
            day = media["startDate"]["day"] if media["startDate"]["day"] is not None else 1
            month = media["startDate"]["month"] if media["startDate"]["month"] is not None else 1
            try :
                media["startDate"] = datetime(media["startDate"]["year"], month, day)
            except:
                media["startDate"] = datetime(media["startDate"]["year"], month, 1)

            # tag processing
            j = 0
            while j < len(media["tags"]):
                if media["tags"][j]["rank"] < 40:
                    media["tags"].pop(j)
                else:
                    j += 1
            
            # score processing
            nb = 0
            media["meanScore"] = 0
            media["scoreVariance"] = 0
            for score in media["stats"]["scoreDistribution"]:
                nb += score["amount"]
                media["meanScore"] += score["score"] * score["amount"]
            media["meanScore"] = ((int) (media["meanScore"] / nb)) if nb > 0 else None
            
            for score in media["stats"]["scoreDistribution"]:
                media["scoreVariance"] += ((score["score"] - media["meanScore"]) ** 2) * score["amount"]
            media["scoreVariance"] = (int) (np.sqrt(media["scoreVariance"] / nb)) if nb > 0 else None

            # supprime l'entrée s'il n'y a eu aucune note 
            if nb < 0:
                rm_list.append(i)

            # status processing
            media["completedWatching"] = 0
            media["planning"] = 0
            media["droppedPaused"] = 0
            for statu in media["stats"]["statusDistribution"]:
                if statu["status"] in ["CURRENT", "COMPLETED"]:
                    media["completedWatching"] += statu["amount"]
                elif statu["status"] == "PLANNING":
                    media["planning"] += statu["amount"]
                elif statu["status"] in ["DROPPED", "PAUSED"]:
                    media["droppedPaused"] += statu["amount"]
            media.pop("stats")

            #staff processing
            media["staffs"] = []
            for i in range(len(media["staff"]["edges"])):
                if pattern.match(media["staff"]["edges"][i]["role"]):
                    staff = {"id": media["staff"]["nodes"][i]["id"], "role": media["staff"]["edges"][i]["role"]}
                    media["staffs"].append(staff)
            media.pop("staff")

            #studio processing
            if "studios" in media:
                media["studio_old"] = media["studios"]
                media["studios"] = []
                for studio in media["studio_old"]["nodes"]:
                    media["studios"].append(studio["id"])
                media.pop("studio_old")

            #cover url 
            media["coverImage"] = media["coverImage"]["large"]

    if len(rm_list) > 0:
        for i in reversed(rm_list):
            medias.pop(i)

    return medias

# listMedia est soit la liste des media MANGA, soit ANIME (pas les 2)
def list_processing_user_infos(listMedia: dict, listFav: dict, mediaType: str):
    formatted_list = []

    # Booléens des oeuvres mises en favories :
    tmp = listFav["User"]["favourites"][mediaType]["nodes"]
    fav_ids = {node["id"] for node in tmp}

    oeuvres = listMedia["MediaListCollection"]["lists"]      
    for list_by_entriesStatus in oeuvres:
        tmp_list = list_by_entriesStatus["entries"] # 1ère list des entries : COMPLETED, 2e : PAUSED, etc.

        for item in tmp_list:
            # Date :
            if item["updatedAt"] != 0 :
                tmp = datetime.fromtimestamp(item["updatedAt"])
                date = str(tmp.day)+"-"+str(tmp.month)+"-"+str(tmp.year)
            elif item["completedAt"]["month"] is None:
                date = str(item["completedAt"]["day"])+"-"+str(item["completedAt"]["month"])+"-"+str(item["completedAt"]["year"])
            else :
                date = str(item["startDate"]["day"])+"-"+str(item["startDate"]["month"])+"-"+str(item["startDate"]["year"])
            
            isFavorite = item["media"]["id"] in fav_ids
            # Other infos :
            formatted_entry = {
                "id": item["media"]["id"],
                "isFavorite": isFavorite, 
                "status": item["status"],
                "score": item["score"],
                "progress": item["progress"],
                "repeat": item["repeat"],
                "date": date
            }

            a=item["media"]["id"]
            # print(f"- - -Id : {a}")
            formatted_list.append(formatted_entry) 
    return formatted_list

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