import os
from pathlib import Path
import glob
import joblib
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient

_MODELS = {}
_VECS = {}
_LAST_ERR = {}

def _resolve_tracking_uri() -> str:
    remote = os.getenv("MLFLOW_TRACKING_URI_REMOTE")
    if remote:
        return remote
    root = Path(__file__).resolve().parents[1]
    mlruns = root / "mlruns"
    return f"file:{mlruns}"

def load_prod_models():
    tracking_uri = _resolve_tracking_uri()
    mlflow.set_tracking_uri(tracking_uri)
    client = MlflowClient()

    for media in ["ANIME", "MANGA"]:
        exp_name = f"reco-{media.lower()}"
        try:
            exp = client.get_experiment_by_name(exp_name)
            if exp is None:
                raise RuntimeError(f"experiment introuvable: {exp_name}")

            runs = client.search_runs(
                experiment_ids=[exp.experiment_id],
                filter_string="tags.deploy = 'prod'",
                order_by=["attributes.start_time DESC"],
                max_results=1,
            )
            if not runs:
                raise RuntimeError(f"aucun run prod pour {exp_name} (tag deploy=prod)")

            run_id = runs[0].info.run_id

            model = mlflow.sklearn.load_model(f"runs:/{run_id}/model")

            vec_dir = mlflow.artifacts.download_artifacts(f"runs:/{run_id}/vectorizer")
            vec_file = glob.glob(str(Path(vec_dir) / "*.joblib"))
            if not vec_file:
                raise RuntimeError("vectorizer .joblib introuvable dans artifacts/vectorizer")
            vec = joblib.load(vec_file[0])

            _MODELS[media] = model
            _VECS[media] = vec
            _LAST_ERR[media] = None

        except Exception as e:
            _LAST_ERR[media] = str(e)

def get(media: str):
    media = media.upper()
    if media not in _MODELS or media not in _VECS:
        raise RuntimeError(f"model non chargé pour {media}. cause: {_LAST_ERR.get(media)}")
    return _MODELS[media], _VECS[media]
