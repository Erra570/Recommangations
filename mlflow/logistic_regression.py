import os
import argparse
import numpy as np
from sqlalchemy import create_engine, text

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score

from pathlib import Path
import mlflow
import mlflow.sklearn
import joblib
import tempfile
import httpx



# ======================
# ARGS
# ======================
parser = argparse.ArgumentParser()
parser.add_argument("--media", choices=["ANIME", "MANGA"], required=True)
args = parser.parse_args()

MEDIA = args.media


# ======================
# CONFIG
# ======================
DATABASE_URL = os.environ["DATABASE_URL"]

ROOT = Path(__file__).resolve().parents[1]
LOCAL_MLRUNS_DIR = ROOT / "mlruns"
LOCAL_TRACKING_URI = f"file:{LOCAL_MLRUNS_DIR}"

REMOTE_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI_REMOTE")

EXPERIMENT_NAME = f"reco-{MEDIA.lower()}"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


def log_run_to_uri(
    tracking_uri: str,
    experiment_name: str,
    media: str,
    model,
    vec,
    n_features: int,
    n_samples: int,
    acc: float,
    f1: float,
) -> dict:
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)

    with mlflow.start_run(run_name=f"logreg-{media.lower()}") as run:
        run_id = run.info.run_id

        mlflow.log_param("media", media)
        mlflow.log_param("model", "logistic_regression")
        mlflow.log_param("n_features", int(n_features))
        mlflow.log_param("n_samples", int(n_samples))

        mlflow.set_tag("deploy", "prod")
        mlflow.set_tag("media", media)

        mlflow.log_metric("accuracy", float(acc))
        mlflow.log_metric("f1", float(f1))

        # Enregistrer le modèle
        model_uri = mlflow.sklearn.log_model(model, artifact_path="model")

        # Enregistrer le vectorizer
        with tempfile.TemporaryDirectory() as td:
            vec_path = Path(td) / "vectorizer.joblib"
            joblib.dump(vec, vec_path)
            mlflow.log_artifact(str(vec_path), artifact_path="vectorizer")

        return {"run_id": run_id, "model_uri": model_uri.model_uri}


# ======================
# SQL QUERY
# ======================

USER_QUERY = """
    SELECT
        id, username
    FROM "user"
"""
if MEDIA == "ANIME":
    QUERY = """
        SELECT
          m.id,
          m.mean_score,
          m.variance_score,
          m.favourites,
          m.format,
          m.country_of_origin,
          extract(epoch from start_date) start,
          COALESCE(array_agg(DISTINCT g.genre_name), '{}') AS genres,
          COALESCE(array_agg(DISTINCT t.tag_id), '{}') AS tags,
          COALESCE(array_agg(DISTINCT s.staff_id), '{}') AS staffs
        FROM anime m 
        LEFT JOIN user_anime u  ON u.anime_id = m.id
        LEFT JOIN anime_genre g ON g.anime_id = m.id
        LEFT JOIN anime_tag t   ON t.anime_id = m.id
        LEFT JOIN anime_staff s ON s.anime_id = m.id
        WHERE CASE WHEN user_id IS NOT NULL THEN true ELSE RANDOM() < 0.005 END
        GROUP BY
          m.id,
          m.mean_score,
          m.variance_score,
          m.favourites,
          m.format,
          m.country_of_origin,
          start
    """
else:
    QUERY = """
        SELECT
          m.id,
          m.mean_score,
          m.variance_score,
          m.favourites,
          m.format,
          m.country_of_origin,
          extract(epoch from start_date) start,
          COALESCE(array_agg(DISTINCT g.genre_name), '{}') AS genres,
          COALESCE(array_agg(DISTINCT t.tag_id), '{}') AS tags,
          COALESCE(array_agg(DISTINCT s.staff_id), '{}') AS staffs
        FROM manga m 
        LEFT JOIN user_manga u  ON u.manga_id = m.id
        LEFT JOIN manga_genre g ON g.manga_id = m.id
        LEFT JOIN manga_tag t   ON t.manga_id = m.id
        LEFT JOIN manga_staff s ON s.manga_id = m.id
        WHERE CASE WHEN user_id IS NOT NULL THEN true ELSE RANDOM() < 0.005 END
        GROUP BY
          m.id,
          m.mean_score,
          m.variance_score,
          m.favourites,
          m.format,
          m.country_of_origin,
          start
    """

def get_user_stat(user_name: str, media: str):
    with httpx.Client(timeout=600.0, transport=httpx.HTTPTransport(retries=2)) as client:
        response = client.get(
            f"http://localhost:8001/api/user/stat/{user_name}/"+str(media).lower(),
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        payload = response.json()
    return payload

# ======================
# LOAD DATA
# ======================
with engine.connect() as c:
    raw_users = c.execute(text(USER_QUERY)).mappings().all()
    medias = c.execute(text(QUERY)).mappings().all()

    # ======================
    # PRE PROCESSING
    # ======================
    users = []
    for raw_user_id in raw_users:
        user_id = dict(raw_user_id)

        user = get_user_stat(user_id["username"], MEDIA)

        users.append(user)
        print(user_id["username"])
        print(user)

# ======================
# BUILD DATASET
# ======================
X_dict = []
y = []

for user in users:
    for media in medias:

        label = 1 if media["id"] in user["have_loved"] else 0

        feats = {
            "delta_mean_score": float(media["mean_score"] or 0) - float(user["mean_mean_score"] or 0),
            "delta_variance_score": float(media["variance_score"] or 0) - float(user["mean_variance_score"] or 0),
            "delta_favourites": float(media["favourites"] or 0) - float(user["mean_favourites"] or 0),
            #"delta_mean_start_date": float(user["mean_start"] or 0) - float(media["start"] or 0),
            "nb_fiting_genres": sum([1 for g in (media.get("genres") or []) if g in user["genre"]]),
            "nb_fiting_tags": sum([1 for g in (media.get("tags") or []) if g in user["tag"]]),
            "country_of_origin_fiting": user[media["country_of_origin"]] if media["country_of_origin"] in user else 0,
            "format_fiting": user[media["format"]] if media["format"] in user else 0
            #, "nb_fiting_staffs": sum([1 for g in (media.get("staffs") or []) if g in user["staff"]])
        }

        X_dict.append(feats)
        y.append(label)

y = np.array(y)

print(f"{MEDIA} nb donnee: {len(y)}")
print(f"{MEDIA} positive rate: {y.mean():.6f}")
print(X_dict[0])

# ======================
# VECTORIZE
# ======================
vec = DictVectorizer(sparse=True)
X = vec.fit_transform(X_dict)


# ======================
# TRAIN / TEST
# ======================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

model = LogisticRegression(
    max_iter=2000,
    class_weight="balanced",
    n_jobs=-1,
)

model.fit(X_train, y_train)

pred = model.predict(X_test)

acc = accuracy_score(y_test, pred)
f1 = f1_score(y_test, pred)

print(f"{MEDIA} accuracy:", acc)
print(f"{MEDIA} f1:", f1)


# ======================
# MLFLOW LOGGING (LOCAL + REMOTE)
# ======================

n_features = X.shape[1]
n_samples = X.shape[0]

run_ids = {}
OUT_DIR = ROOT / "mlflow_outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

joblib.dump(model, OUT_DIR / f"logreg_{MEDIA.lower()}.joblib")
joblib.dump(vec, OUT_DIR / f"vectorizer_{MEDIA.lower()}.joblib")

local_run_id = log_run_to_uri(
    tracking_uri=LOCAL_TRACKING_URI,
    experiment_name=EXPERIMENT_NAME,
    media=MEDIA,
    model=model,
    vec=vec,
    n_features=n_features,
    n_samples=n_samples,
    acc=acc,
    f1=f1,
)
run_ids["local"] = local_run_id

"""if REMOTE_TRACKING_URI:
    remote_run_id = log_run_to_uri(
        tracking_uri=REMOTE_TRACKING_URI,
        experiment_name=EXPERIMENT_NAME,
        media=MEDIA,
        model=model,
        vec=vec,
        n_features=n_features,
        n_samples=n_samples,
        acc=acc,
        f1=f1,
    )
    run_ids["remote"] = remote_run_id"""

print(f"{MEDIA} logged to LOCAL MLflow: {LOCAL_TRACKING_URI} (run_id = {run_ids['local']['run_id']}) (model_id = {run_ids['local']['model_uri']})")
if "remote" in run_ids:
    print(f"{MEDIA} logged to REMOTE MLflow: {REMOTE_TRACKING_URI} (run_id={run_ids['remote']})")
else:
    print("REMOTE not logged (set MLFLOW_TRACKING_URI_REMOTE to enable).")
