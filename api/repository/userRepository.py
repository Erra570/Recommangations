from models import *
from db import get_db
from sqlalchemy import text
from .queries import *

def get_user_stat(id:int, media):
	for session in get_db():
		raw_users = session.execute(text(USER_QUERY(media)), {"user_id": id}).mappings().all()

		for raw_user in raw_users:
			user = dict(raw_user)

			user["genre"] = []
			users_genres = session.execute(text(USER_GENRE_QUERY(media)), {"user_id": id}).mappings().all()
			for genre in users_genres:
				if(genre["nb"] >= user["nb"]/4):
					user["genre"].append(genre["genre_name"])
				else:
					break
			
			user["tag"] = []
			users_tags = session.execute(text(USER_TAG_QUERY(media)), {"user_id": id}).mappings().all()
			for tag in users_tags:
				print(user["nb"])
				print(tag["nb"])
				print(tag)
				if(tag["nb"] >= user["nb"]/4):
					user["tag"].append(tag["tag_id"])
				else:
					break
			
			user["staff"] = []
			users_staffs = session.execute(text(USER_STAFF_QUERY(media)), {"user_id": id}).mappings().all()
			for staff in users_staffs:
				if(staff["nb"] > 0.8):
					user["staff"].append(staff["staff_id"])
				else:
					break

			user["have_loved"] = []
			users_loved = session.execute(text(USER_MEDIA_QUERY(media)), {"user_id": id}).mappings().all()
			for user_loved in users_loved:
				user["have_loved"].append(user_loved["media_id"])
			
			country_of_origin_sum = 0.0
			users_country_of_origins = session.execute(text(USER_COUNTRY_OF_ORIGIN_QUERY(media)), {"user_id": id}).mappings().all()
			for country_of_origin in users_country_of_origins:
				print(country_of_origin["country_of_origin"])
				print(country_of_origin["nb"])
				country_of_origin_sum += country_of_origin["nb"]
			for country_of_origin in users_country_of_origins:
				user[country_of_origin["country_of_origin"]] = country_of_origin["nb"]/country_of_origin_sum
			
			format_sum = 0.0
			users_formats = session.execute(text(USER_FORMAT_QUERY(media)), {"user_id": id}).mappings().all()
			for format in users_formats:
				format_sum += format["nb"]
			for format in users_formats:
				user[format["format"]] = format["nb"]/format_sum

			return user