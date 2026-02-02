from fastapi.testclient import TestClient
import pytest

from api.main import app, api_router

### - - - Tests généraux (du main.py, etc) - - -

client = TestClient(app)
client_api = TestClient(api_router)

def test_root_health():
    rep = client.get("/health")
    assert rep.status_code == 200
    assert rep.json() == {"status": "ok"}

def test_api_health():
    rep = client_api.get("/health")
    assert rep.status_code == 200
    assert rep.json() == {"status": "ok"}

def test_metrics():
    rep = client.get("/metrics")
    assert rep.status_code == 200