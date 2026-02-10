import joblib
import glob
from pathlib import Path
import mlflow
import mlflow.sklearn

RUN_ID = {
    "MANGA" : "a4b4f77b762142ef986cd1b763f6399d",
    "ANIME" : "a4b4f77b762142ef986cd1b763f6399d"
}

MODEL_ID = {
    "MANGA" : "m-5abefda99ce74d0590d80f59d5887971",
    "ANIME" : "m-5abefda99ce74d0590d80f59d5887971"
}

_MODELS = {}
_VECS = {}

def load_models_from_disk():
    d = "./mlflow_outputs"

    for media in ["ANIME", "MANGA"]:
        mpath = Path(d + "/" + f"logreg_{media.lower()}.joblib")
        vpath = Path(d + "/" + f"vectorizer_{media.lower()}.joblib")

        if not mpath.exists() or not vpath.exists():
            raise RuntimeError(f"missing files for {media}: {mpath} / {vpath}")
        
        _MODELS[media] = joblib.load(mpath)
        _VECS[media] = joblib.load(vpath)
        """
        model_uri = "file:./mlruns/134715072494730965/models/"+MODEL_ID[media]+"/artifacts"
        model = mlflow.sklearn.load_model(model_uri)

        #vec_dir = mlflow.artifacts.download_artifacts(f"runs:/{run_id}/vectorizer")
        artifact_uri = "file:./mlruns/134715072494730965/"+RUN_ID[media]+"/artifacts/vectorizer"	
        vec_dir = mlflow.artifacts.download_artifacts(artifact_uri)
        vec_file = glob.glob(str(Path(vec_dir) / "*.joblib"))
        if not vec_file:
            raise RuntimeError("vectorizer .joblib introuvable dans artifacts/vectorizer")
        vec = joblib.load(vec_file[0])

        _MODELS[media] = model
        _VECS[media] = vec"""

def get(media: str):
    media = media.upper()
    if media not in _MODELS or media not in _VECS:
        raise RuntimeError(f"model not loaded for {media}. call load_models_from_disk() first")
    return _MODELS[media], _VECS[media]
