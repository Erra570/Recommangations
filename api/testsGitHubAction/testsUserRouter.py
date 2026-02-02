import pytest
from fastapi.testclient import TestClient

from userRouter import router as user_router 

### - - - Tests sur userRouter.py - - -

client_api_user = TestClient(user_router)

unknown__user       = {"user_id": None, "username": "trdcfgvyulhjgfvhyboljcsdv"} # on va esperer que PERSONNE ne récup ce username hein
existing_user       = {"user_id": 6960032, "username": "voidhi"}
true_manga_fav_id   = 98263  # (pour le succès et le futur de ces tests GitHubAction, je jure ne jamais retirer ces deux de mes favs...)
true_anime_fav_id   = 137667
completed_manga_id  = 33031 # comme les completed sont en list[0]
completed_anime_id  = 137667



def test_get_user_id():
    rep = client_api_user.get(f"/{existing_user['username']}")
    assert rep.status_code == 200
    assert rep.json() == existing_user

    rep = client_api_user.get(f"/{unknown__user['username']}")
    assert rep.status_code == 500


def test_get_user_favorites():
    rep = client_api_user.get(f"/{existing_user['username']}/favorites")
    rep_json = rep.json()

    assert rep.status_code == 200
    assert "User" in rep_json

    fav_manga_ids_list = [d["id"] for d in rep_json["User"]["favourites"]["manga"]["nodes"]]
    fav_anime_ids_list = [d["id"] for d in rep_json["User"]["favourites"]["anime"]["nodes"]]

    assert true_manga_fav_id in fav_manga_ids_list
    assert true_anime_fav_id in fav_anime_ids_list


def test_get_user_entries():
    rep = client_api_user.get(f"/{existing_user['username']}/entries/MANGA")
    rep_json = rep.json()
    assert rep.status_code == 200
    assert "MediaListCollection" in rep_json
    entries_manga_ids_list = []
    for l in rep_json["MediaListCollection"]["lists"]:
        for entry in l["entries"]:
            entries_manga_ids_list.append(entry["media"]["id"])

    rep = client_api_user.get(f"/{existing_user['username']}/entries/ANIME")
    rep_json = rep.json()
    assert rep.status_code == 200
    assert "MediaListCollection" in rep_json
    entries_anime_ids_list = []
    for l in rep_json["MediaListCollection"]["lists"]:
        for entry in l["entries"]:
            entries_anime_ids_list.append(entry["media"]["id"])

    assert true_manga_fav_id in entries_manga_ids_list
    assert true_anime_fav_id in entries_anime_ids_list