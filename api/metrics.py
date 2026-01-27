from prometheus_client import Counter, Histogram, Gauge

# Counters :
USER_ID_REQUESTS = Counter(
    "user_id_requests_total",
    "Counter du nombre de UserId recherchés à partir d'un UserName"
)

ANILIST_ERRORS = Counter(
    "anilist_errors_total",
    "Total number of AniList API errors"
)

# Histograms
ANIME_LIST_DURATION = Histogram(
    "anime_list_request_duration_seconds",
    "Temps écoulée durant une requête de fetch /list/anime ",
    buckets=(0.2, 2, 5, 10) # plages de temps (rapide, ok, lent, pb......)
)

# Gauges :
 