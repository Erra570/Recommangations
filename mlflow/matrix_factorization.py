import os
import argparse
import numpy as np
from sqlalchemy import create_engine, text
from pathlib import Path
import tempfile
import joblib
import mlflow

from scipy.sparse import coo_matrix, csr_matrix

# Modèle MF (implicit)
from implicit.als import AlternatingLeastSquares


# ======================
# ARGS
# ======================
parser = argparse.ArgumentParser()
parser.add_argument("--media", choices=["ANIME", "MANGA"], required=True)

# Hyperparams ALS
parser.add_argument("--factors", type=int, default=64)
parser.add_argument("--iterations", type=int, default=30)
parser.add_argument("--regularization", type=float, default=0.05)

# Pondération implicit (confiance)
parser.add_argument("--alpha", type=float, default=20.0)

# Evaluation rapide
parser.add_argument("--eval_k", type=int, default=20)
parser.add_argument("--eval_users", type=int, default=2000)  # limiter pour accélérer
parser.add_argument("--seed", type=int, default=42)

args = parser.parse_args()
MEDIA = args.media

rng = np.random.default_rng(args.seed)


# ======================
# CONFIG
# ======================
DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

ROOT = Path(__file__).resolve().parents[1]
LOCAL_MLRUNS_DIR = ROOT / "mlruns"
LOCAL_TRACKING_URI = f"file:{LOCAL_MLRUNS_DIR}"

REMOTE_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI_REMOTE")
EXPERIMENT_NAME = f"reco-{MEDIA.lower()}"  # pour rester cohérent avec ton projet


# ======================
# SQL QUERY (interactions)
# ======================
# On apprend à partir de la table user_anime / user_manga :
# - user_id
# - media_id
# - score / progress / status
#
# NB: On n’a pas besoin des genres ici : MF apprend des facteurs latents user×item.
if MEDIA == "ANIME":
    QUERY = """
        SELECT
          ua.user_id,      
          u.username,              
          ua.anime_id AS media_id,
          ua.score,
          ua.progress,
          ua.status
        FROM user_anime ua
        JOIN users u ON u.id = ua.user_id
    """
else:
    QUERY = """
        SELECT
          um.user_id,
          u.username,
          um.manga_id AS media_id,
          um.score,
          um.progress,
          um.status
        FROM user_manga um
        JOIN users u ON u.id = um.user_id
    """


# ======================
# LOAD DATA
# ======================
with engine.connect() as c:
    rows = c.execute(text(QUERY)).mappings().all()

if len(rows) < 50:
    raise RuntimeError(f"Pas assez de données pour {MEDIA} ({len(rows)} rows)")

print(f"{MEDIA} interactions loaded: {len(rows)}")


# ======================
# BUILD IMPLICIT FEEDBACK
# ======================
# On transforme (score/progress/status) en "strength" (poids) >= 0
#
# Idée simple et robuste :
# - base = 1
# - +2 si COMPLETED
# - + (score/10) si score present
# - + min(progress/50, 1) pour signaler consommation
#
# Ensuite on met la "confidence" = 1 + alpha * strength (standard implicit ALS)
def interaction_strength(r) -> float:
    s = 1.0
    status = (r["status"] or "").upper()
    if status == "COMPLETED":
        s += 2.0
    score = r["score"]
    if score is not None:
        s += float(score) / 10.0  # score AniList souvent sur 10
    prog = r["progress"] or 0
    s += min(float(prog) / 50.0, 1.0)
    return max(s, 0.0)


# On construit des listes user_id/media_id/weight
user_ids = []
media_ids = []
weights = []

for r in rows:
    uid = r["user_id"]
    mid = r["media_id"]
    if uid is None or mid is None:
        continue
    w = interaction_strength(r)
    # garder uniquement les interactions non-nulles
    if w <= 0:
        continue
    user_ids.append(int(uid))
    media_ids.append(int(mid))
    weights.append(float(w))

if len(weights) < 50:
    raise RuntimeError(f"Pas assez d'interactions exploitables pour {MEDIA} ({len(weights)})")

print(f"{MEDIA} usable interactions: {len(weights)}")


# ======================
# ID MAPPINGS (stable within run)
# ======================
# ALS veut des indices 0..n-1
uniq_users = np.array(sorted(set(user_ids)), dtype=np.int64)
uniq_items = np.array(sorted(set(media_ids)), dtype=np.int64)

user_id_to_idx = {int(u): int(i) for i, u in enumerate(uniq_users)}
item_id_to_idx = {int(it): int(j) for j, it in enumerate(uniq_items)}
idx_to_item_id = {int(j): int(it) for j, it in enumerate(uniq_items)}

n_users = len(uniq_users)
n_items = len(uniq_items)

print(f"{MEDIA} n_users={n_users} n_items={n_items}")


# ======================
# BUILD SPARSE MATRIX (users x items)
# ======================
u_idx = np.array([user_id_to_idx[u] for u in user_ids], dtype=np.int64)
i_idx = np.array([item_id_to_idx[it] for it in media_ids], dtype=np.int64)
w = np.array(weights, dtype=np.float32)

# Confidence matrix (users x items)
# implicit ALS utilise un schéma "confidence = 1 + alpha * r_ui"
conf = 1.0 + args.alpha * w

user_items = coo_matrix((conf, (u_idx, i_idx)), shape=(n_users, n_items)).tocsr()


# ======================
# SIMPLE HOLDOUT EVAL (Recall@K)
# ======================
# On fait un split "leave-one-out" par utilisateur :
# - pour chaque user avec >=2 interactions: on retire 1 item en test
# - on entraîne sur le reste
#
# Ceci n’est pas une évaluation parfaite, mais c’est utile pour valider que ça marche.
def build_train_test_leave_one_out(mat: csr_matrix, max_users: int):
    mat = mat.tocsr()
    all_users = np.arange(mat.shape[0])
    users = all_users
    if max_users and len(all_users) > max_users:
        users = rng.choice(all_users, size=max_users, replace=False)

    test_pairs = []  # (u, heldout_item)
    train = mat.copy().tolil()

    for u in users:
        start, end = mat.indptr[u], mat.indptr[u + 1]
        items_u = mat.indices[start:end]
        if len(items_u) < 2:
            continue
        heldout = int(rng.choice(items_u))
        # retirer dans train
        # (si plusieurs entrées, LIL simplifie)
        train[u, heldout] = 0.0
        test_pairs.append((int(u), heldout))

    train = train.tocsr()
    train.eliminate_zeros()
    return train, test_pairs

train_mat, test_pairs = build_train_test_leave_one_out(user_items, args.eval_users)
print(f"{MEDIA} eval users (with holdout): {len(test_pairs)}")


# ======================
# TRAIN ALS
# ======================
# implicit attend une matrice item-user (items x users)
item_users = train_mat.T.tocsr()

model = AlternatingLeastSquares(
    factors=args.factors,
    iterations=args.iterations,
    regularization=args.regularization,
    random_state=args.seed,
)

model.fit(item_users)


# ======================
# EVAL Recall@K
# ======================
def recall_at_k(model, train_user_items: csr_matrix, test_pairs, k: int) -> float:
    if not test_pairs:
        return 0.0

    hits = 0
    # recommend() attend user_items (users x items)
    for u, heldout_item in test_pairs:
        # model.recommend renvoie des indices d'items
        rec_items, _ = model.recommend(
            userid=u,
            user_items=train_user_items,
            N=k,
            filter_already_liked_items=True,
            recalculate_user=True,
        )
        if int(heldout_item) in set(map(int, rec_items)):
            hits += 1

    return hits / len(test_pairs)

recall_k = recall_at_k(model, train_mat, test_pairs, args.eval_k)
print(f"{MEDIA} Recall@{args.eval_k}: {recall_k:.4f}")


# ======================
# MLFLOW LOGGING
# ======================
def log_run_to_uri(tracking_uri: str) -> str:
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(EXPERIMENT_NAME)

    with mlflow.start_run(run_name=f"als-{MEDIA.lower()}") as run:
        run_id = run.info.run_id

        # params
        mlflow.log_param("media", MEDIA)
        mlflow.log_param("model", "implicit_als")
        mlflow.log_param("factors", int(args.factors))
        mlflow.log_param("iterations", int(args.iterations))
        mlflow.log_param("regularization", float(args.regularization))
        mlflow.log_param("alpha", float(args.alpha))
        mlflow.log_param("n_users", int(n_users))
        mlflow.log_param("n_items", int(n_items))

        # tags (important pour model_store)
        mlflow.set_tag("deploy", "prod")
        mlflow.set_tag("media", MEDIA)
        mlflow.set_tag("algo", "als")

        # metrics
        mlflow.log_metric(f"recall_at_{args.eval_k}", float(recall_k))

        # artefacts
        # On log :
        # - modèle ALS
        # - mappings user/item
        # - (optionnel) matrice train (souvent lourd, donc on l’évite)
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)

            model_path = td / "als_model.joblib"
            joblib.dump(model, model_path)
            mlflow.log_artifact(str(model_path), artifact_path="model")

            maps_path = td / "mappings.joblib"
            joblib.dump(
                {
                    "user_id_to_idx": user_id_to_idx,
                    "item_id_to_idx": item_id_to_idx,
                    "idx_to_item_id": idx_to_item_id,
                },
                maps_path,
            )
            mlflow.log_artifact(str(maps_path), artifact_path="mappings")

        return run_id


local_run_id = log_run_to_uri(LOCAL_TRACKING_URI)
print(f"{MEDIA} logged to LOCAL MLflow: {LOCAL_TRACKING_URI} (run_id={local_run_id})")

if REMOTE_TRACKING_URI:
    remote_run_id = log_run_to_uri(REMOTE_TRACKING_URI)
    print(f"{MEDIA} logged to REMOTE MLflow: {REMOTE_TRACKING_URI} (run_id={remote_run_id})")
else:
    print("REMOTE not logged (set MLFLOW_TRACKING_URI_REMOTE to enable).")
