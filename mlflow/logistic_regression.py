import os
import json
import math
import argparse

import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score

import mlflow


def read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_total_len(media, media_type):
    key = "episodes" if media_type == "ANIME" else "chapters"
    v = media.get(key)
    return v if isinstance(v, int) and v > 0 else None


def make_label(entry, total_len, pos_score=7.0, pos_ratio=0.6):
    if entry.get("isFavorite") is True:
        return 1

    score = entry.get("score", 0)
    try:
        score = float(score)
    except Exception:
        score = 0.0
    if score >= pos_score:
        return 1

    status = str(entry.get("status") or "").upper()
    if status == "COMPLETED":
        return 1

    progress = entry.get("progress", 0)
    try:
        progress = int(progress)
    except Exception:
        progress = 0

    if total_len:
        if (progress / float(total_len)) >= pos_ratio:
            return 1

    return 0


def build_user_profile(catalog_by_id, user_ids, y, media_type):
    liked_ids = [mid for mid, lab in zip(user_ids, y) if lab == 1]
    if not liked_ids:
        return {"genres": set(), "len_mean": 0.0, "fmt_counts": {}}

    genres = set()
    lengths = []
    fmt_counts = {}

    for mid in liked_ids:
        m = catalog_by_id.get(mid)
        if not m:
            continue

        for g in (m.get("genres") or []):
            if g:
                genres.add(str(g))

        t = get_total_len(m, media_type)
        if t:
            lengths.append(t)

        fmt = m.get("format")
        if fmt:
            fmt = str(fmt)
            fmt_counts[fmt] = fmt_counts.get(fmt, 0) + 1

    len_mean = float(np.mean(lengths)) if lengths else 0.0
    return {"genres": genres, "len_mean": len_mean, "fmt_counts": fmt_counts}


def make_features(media, profile, media_type, user_weight=4.0, global_weight=0.15):
    feats = {}


    gset = set(str(g) for g in (media.get("genres") or []) if g)
    inter = len(gset & profile["genres"])
    union = len(gset | profile["genres"]) if (profile["genres"] or gset) else 0
    feats["u_genre_overlap"] = user_weight * float(inter)
    feats["u_genre_jaccard"] = user_weight * (float(inter) / float(union) if union else 0.0)

    t = get_total_len(media, media_type)
    if t and profile["len_mean"] > 0:
        diff = abs(float(t) - profile["len_mean"])
        feats["u_len_close"] = user_weight * (1.0 / (1.0 + diff))  # plus grand = plus proche
    else:
        feats["u_len_close"] = 0.0

    fmt = media.get("format")
    if fmt:
        fmt = str(fmt)
        feats["u_format_pref"] = user_weight * float(profile["fmt_counts"].get(fmt, 0))
    else:
        feats["u_format_pref"] = 0.0

    ms = media.get("meanScore")
    if isinstance(ms, (int, float)):
        feats["g_meanScore"] = global_weight * (float(ms) / 100.0)

    fav = media.get("favourites")
    if isinstance(fav, int) and fav > 0:
        feats["g_log_fav"] = global_weight * (math.log1p(fav) / math.log1p(200000))

    return feats


def main():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    data_dir = os.path.join(root, "data")
    out_dir = os.path.join(root, "mlflow_outputs")
    os.makedirs(out_dir, exist_ok=True)

    p = argparse.ArgumentParser()
    p.add_argument("--media_type", choices=["ANIME", "MANGA"], default="ANIME")

    p.add_argument("--user_weight", type=float, default=4.0)
    p.add_argument("--global_weight", type=float, default=0.15)

    p.add_argument("--pos_score", type=float, default=7.0)
    p.add_argument("--pos_ratio", type=float, default=0.6)

    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--C", type=float, default=1.0)

    p.add_argument("--top_n", type=int, default=20)

    p.add_argument("--experiment", type=str, default="reco-logreg-simple")

    args = p.parse_args()

    if args.media_type == "ANIME":
        catalog_path = os.path.join(data_dir, "anime.json")
        user_path = os.path.join(data_dir, "userAnime.json")
    else:
        catalog_path = os.path.join(data_dir, "manga.json")
        user_path = os.path.join(data_dir, "userManga.json")

    catalog = read_json(catalog_path)
    user_entries = read_json(user_path)

    catalog_by_id = {m["id"]: m for m in catalog if isinstance(m, dict) and isinstance(m.get("id"), int)}

    user_ids = []
    y = []
    for e in user_entries:
        mid = e.get("id")
        if not isinstance(mid, int):
            continue
        m = catalog_by_id.get(mid)
        if not m:
            continue
        lab = make_label(e, get_total_len(m, args.media_type), pos_score=args.pos_score, pos_ratio=args.pos_ratio)
        user_ids.append(mid)
        y.append(lab)

    if len(y) < 30 or len(set(y)) < 2:
        print("Pas assez d'exemples labellisés (vise >= 30 et des labels 0/1).")
        print("Solutions: baisser pos_score (ex 6.5) ou pos_ratio (ex 0.5), ou récupérer plus d'entries user.")
        return

    profile = build_user_profile(catalog_by_id, user_ids, y, args.media_type)

    X = [make_features(catalog_by_id[mid], profile, args.media_type, args.user_weight, args.global_weight) for mid in user_ids]

    vec = DictVectorizer(sparse=True)
    Xv = vec.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        Xv, np.array(y), test_size=0.2, random_state=args.seed, stratify=np.array(y)
    )

    model = LogisticRegression(max_iter=400, C=args.C, class_weight="balanced")
    model.fit(X_train, y_train)

    pred = model.predict(X_test)
    metrics = {
        "accuracy": float(accuracy_score(y_test, pred)),
        "f1": float(f1_score(y_test, pred)),
        "precision": float(precision_score(y_test, pred, zero_division=0)),
        "recall": float(recall_score(y_test, pred, zero_division=0)),
        "n_train": int(len(y_train)),
        "n_test": int(len(y_test)),
        "n_features": int(Xv.shape[1]),
        "pos_rate": float(np.mean(y)),
    }

    seen = set(user_ids)
    cand = []
    Xc = []
    for m in catalog:
        mid = m.get("id")
        if not isinstance(mid, int) or mid in seen:
            continue
        cand.append(m)
        Xc.append(make_features(m, profile, args.media_type, args.user_weight, args.global_weight))

    recs = []
    if cand:
        Xcv = vec.transform(Xc)
        probs = model.predict_proba(Xcv)[:, 1]
        idx = np.argsort(-probs)[: args.top_n]
        for i in idx:
            m = cand[int(i)]
            t = m.get("title") if isinstance(m.get("title"), dict) else {}
            title = (t.get("romaji") or t.get("english")) if isinstance(t, dict) else None
            recs.append({"id": m.get("id"), "title": title, "prob_like": float(probs[int(i)])})

    model_path = os.path.join(out_dir, f"logreg_{args.media_type.lower()}.joblib")
    vec_path = os.path.join(out_dir, f"vectorizer_{args.media_type.lower()}.joblib")
    recs_path = os.path.join(out_dir, f"recs_{args.media_type.lower()}.json")

    import joblib
    joblib.dump(model, model_path)
    joblib.dump(vec, vec_path)
    with open(recs_path, "w", encoding="utf-8") as f:
        json.dump(recs, f, indent=2, ensure_ascii=False)

    print("metrics:", metrics)
    print("saved:", model_path)
    print("saved:", vec_path)
    print("saved:", recs_path)
    print("top recs:")
    for r in recs[:10]:
        print("-", r["title"], "prob", round(r["prob_like"], 3))
    mlflow.set_tracking_uri("http://localhost:5001")
    mlflow.set_experiment(args.experiment)
    with mlflow.start_run():
        mlflow.log_params(
            {
                "media_type": args.media_type,
                "user_weight": args.user_weight,
                "global_weight": args.global_weight,
                "pos_score": args.pos_score,
                "pos_ratio": args.pos_ratio,
                "C": args.C,
                "seed": args.seed,
            }
        )
        mlflow.log_metrics({k: float(v) for k, v in metrics.items() if k in ["accuracy", "f1", "precision", "recall"]})
        mlflow.log_artifact(model_path)
        mlflow.log_artifact(vec_path)
        mlflow.log_artifact(recs_path)


if __name__ == "__main__":
    main()