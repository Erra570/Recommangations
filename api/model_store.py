import joblib
from pathlib import Path

_MODELS = {}
_VECS = {}

def load_models_from_disk():
    root = Path(__file__).resolve().parents[1]
    d = root / "mlflow_outputs"

    for media in ["ANIME", "MANGA"]:
        mpath = d / f"logreg_{media.lower()}.joblib"
        vpath = d / f"vectorizer_{media.lower()}.joblib"

        if not mpath.exists() or not vpath.exists():
            raise RuntimeError(f"missing files for {media}: {mpath} / {vpath}")

        _MODELS[media] = joblib.load(mpath)
        _VECS[media] = joblib.load(vpath)

def get(media: str):
    media = media.upper()
    if media not in _MODELS or media not in _VECS:
        raise RuntimeError(f"model not loaded for {media}. call load_models_from_disk() first")
    return _MODELS[media], _VECS[media]
