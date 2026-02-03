import pytest
from fastapi.testclient import TestClient

from main import app

### - - - Tests sur userRouter.py - - -

client = TestClient(app)

unknown__user       = {"user_id": None, "username": "trdcfgvyulhjgfvhyboljcsdv"} # on va esperer que PERSONNE ne récup ce username hein
existing_user       = {"user_id": 6960032, "username": "Voidhi"}
true_manga_fav_id   = 98263  # (pour le succès et le futur de ces tests GitHubAction, je jure ne jamais retirer ces deux de mes favs...)
true_anime_fav_id   = 137667
completed_manga_id  = 33031 
completed_anime_id  = 137667



def test_get_user_id():
    rep = client.get(f"/api/user/{existing_user['username']}")
    assert rep.status_code == 200
    assert rep.json() == existing_user

    rep = client.get(f"/api/user/{unknown__user['username']}")
    assert rep.status_code == 200 # renvoit quand même un 200 si user introuvable


def test_get_user_favorites():
    rep = client.get(f"/api/user/{existing_user['username']}/favorites")
    rep_json = rep.json()

    assert rep.status_code == 200
    assert "User" in rep_json

    fav_manga_ids_list = [d["id"] for d in rep_json["User"]["favourites"]["manga"]["nodes"]]
    fav_anime_ids_list = [d["id"] for d in rep_json["User"]["favourites"]["anime"]["nodes"]]

    assert true_manga_fav_id in fav_manga_ids_list
    assert true_anime_fav_id in fav_anime_ids_list


def test_get_user_entries():
    # Manga entries :
    rep = client.get(f"/api/user/{existing_user['username']}/entries/MANGA")
    rep_json = rep.json()
    assert rep.status_code == 200

    entries_manga_ids_list = [entry["id"] for entry in rep_json]
    assert completed_manga_id in entries_manga_ids_list

    # Anime entries :
    rep = client.get(f"/api/user/{existing_user['username']}/entries/ANIME")
    rep_json = rep.json()
    assert rep.status_code == 200
    
    entries_anime_ids_list = [entry["id"] for entry in rep_json]
    assert completed_anime_id in entries_anime_ids_list