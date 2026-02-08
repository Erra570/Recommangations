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
) -> str:
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)

    with mlflow.start_run(run_name=f"logreg-{media.lower()}") as run:
        run_id = run.info.run_id

        mlflow.log_param("media", media)
        mlflow.log_param("model", "logistic_regression")
        mlflow.log_param("n_features", int(n_features))
        mlflow.log_param("n_samples", int(n_samples))
        mlflow.log_param("tag_min_df", int(TAG_MIN_DF))

        mlflow.set_tag("deploy", "prod")
        mlflow.set_tag("media", media)

        mlflow.log_metric("accuracy", float(acc))
        mlflow.log_metric("f1", float(f1))

        mlflow.sklearn.log_model(model, artifact_path="model")

        # vectorizer
        with tempfile.TemporaryDirectory() as td:
            vec_path = Path(td) / "vectorizer.joblib"
            joblib.dump(vec, vec_path)
            mlflow.log_artifact(str(vec_path), artifact_path="vectorizer")

        return run_id


def load_allowed_tags(engine, media: str, top_k: int = 300) -> set:
    if media == "ANIME":
        q = """
            SELECT DISTINCT ON (at.tag_id)
                   t.name AS tag_name,
                   at.rank
            FROM anime_tag at
            JOIN tag t ON t.id = at.tag_id
            ORDER BY at.tag_id, at.rank DESC
            LIMIT :top_k
        """
    else:
        q = """
            SELECT DISTINCT ON (mt.tag_id)
                   t.name AS tag_name,
                   mt.rank
            FROM manga_tag mt
            JOIN tag t ON t.id = mt.tag_id
            ORDER BY mt.tag_id, mt.rank DESC
            LIMIT :top_k
        """

    with engine.connect() as c:
        tag_rows = c.execute(
            text(q),
            {"top_k": top_k}
        ).mappings().all()

    allowed = {r["tag_name"] for r in tag_rows}
    return allowed


# ======================
# SQL QUERY
# ======================
if MEDIA == "ANIME":
    QUERY = """
        SELECT
          ua.user_id,
          ua.anime_id AS media_id,
          ua.score,
          ua.progress,
          ua.status,
          a.mean_score,
          a.favourites,
          COALESCE(array_agg(DISTINCT ag.genre_name), '{}') AS genres,
          COALESCE(array_agg(DISTINCT t.name), '{}') AS tags
        FROM user_anime ua
        JOIN anime a ON a.id = ua.anime_id
        LEFT JOIN anime_genre ag ON ag.anime_id = a.id
        LEFT JOIN anime_tag at ON at.anime_id = a.id
        LEFT JOIN tag t ON t.id = at.tag_id
        GROUP BY
          ua.user_id,
          ua.anime_id,
          ua.score,
          ua.progress,
          ua.status,
          a.mean_score,
          a.favourites
    """
else:
    QUERY = """
        SELECT
          um.user_id,
          um.manga_id AS media_id,
          um.score,
          um.progress,
          um.status,
          m.mean_score,
          m.favourites,
          COALESCE(array_agg(DISTINCT mg.genre_name), '{}') AS genres,
          COALESCE(array_agg(DISTINCT t.name), '{}') AS tags
        FROM user_manga um
        JOIN manga m ON m.id = um.manga_id
        LEFT JOIN manga_genre mg ON mg.manga_id = m.id
        LEFT JOIN manga_tag mt ON mt.manga_id = m.id
        LEFT JOIN tag t ON t.id = mt.tag_id
        GROUP BY
          um.user_id,
          um.manga_id,
          um.score,
          um.progress,
          um.status,
          m.mean_score,
          m.favourites
    """


# ======================
# LOAD DATA
# ======================
with engine.connect() as c:
    rows = c.execute(text(QUERY)).mappings().all()

if len(rows) < 50:
    raise RuntimeError(f"Pas assez de données pour {MEDIA} ({len(rows)} rows)")

print(f"{MEDIA} rows loaded: {len(rows)}")

TOP_K_TAGS = int(os.getenv("TOP_K_TAGS", "300"))
allowed_tags = load_allowed_tags(engine, MEDIA, top_k=TOP_K_TAGS)
print(f"{MEDIA} allowed tags (top_k={TOP_K_TAGS}): {len(allowed_tags)}")


# ======================
# BUILD DATASET
# ======================
X_dict = []
y = []

for r in rows:
    label = 1 if (
        (r["status"] == "COMPLETED" or r["status"] == "READING") and (r["score"] is None or r["score"] >= 7)
    ) else 0

    feats = {
        "mean_score": float(r["mean_score"] or 0),
        "log_favourites": float(np.log1p(r["favourites"] or 0)),
    }

    for g in (r.get("genres") or []):
        if g:
            feats[f"genre_{g}"] = 1

    for t in (r.get("tags") or []):
        if t and t in allowed_tags:
            feats[f"tag_{t}"] = 1

    X_dict.append(feats)
    y.append(label)

y = np.array(y)

print(f"{MEDIA} positive rate: {y.mean():.3f}")


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

if REMOTE_TRACKING_URI:
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
    run_ids["remote"] = remote_run_id

print(f"{MEDIA} logged to LOCAL MLflow: {LOCAL_TRACKING_URI} (run_id={run_ids['local']})")
if "remote" in run_ids:
    print(f"{MEDIA} logged to REMOTE MLflow: {REMOTE_TRACKING_URI} (run_id={run_ids['remote']})")
else:
    print("REMOTE not logged (set MLFLOW_TRACKING_URI_REMOTE to enable).")