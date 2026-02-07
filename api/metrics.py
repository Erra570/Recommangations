from prometheus_client import Counter, Histogram, Gauge

# Counters :
USER_ID_REQUESTS = Counter(
    "user_id_requests_total",
    "Counter du nombre de UserId recherchés à partir d'un UserName",
    ["status"] #succes/echec
)

ANILIST_ERRORS = Counter(
    "anilist_errors_total",
    "Nb total d'erreurs de l'API d'Anilist",
    ["error_type"]
)

# Histograms
ANIME_LIST_DURATION = Histogram(
    "anime_list_request_duration_seconds",
    "Temps écoulée durant une requête de fetch /list/anime ",
    buckets=(0.2, 2, 5, 10) # plages de temps (rapide, ok, lent, pb......)
)

DATABASE_UPDATE_ALL_DURATION = Histogram(
    "database_update_all_request_duration_seconds",
    "Temps écoulée lors d'un update de la DB (/update)",
    buckets=(0.2, 5, 60, 120)
)

DATABASE_UPDATE_ANIME_DURATION = Histogram(
    "database_update_anime_request_duration_seconds",
    "Temps écoulée lors d'un update de la DB (/update/anime)",
    buckets=(0.2, 5, 60, 120)
)
DATABASE_UPDATE_MANGA_DURATION = Histogram(
    "database_update_manga_request_duration_seconds",
    "Temps écoulée lors d'un update de la DB (/update/manga)",
    buckets=(0.2, 5, 60, 120)
)

# Gauges :
DATABASE_UPDATE_ALL_LAST_DURATION = Gauge(
    "database_update_all_last_request_duration_seconds",
    "Temps écoulée lors de la DERNIERE update de la DB (/update)"
)