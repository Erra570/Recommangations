from fastapi.testclient import TestClient
import pytest

from main import app

### - - - Tests généraux (du main.py, etc) - - -

client = TestClient(app)

def test_root_health():
    rep = client.get("/health")
    assert rep.status_code == 200
    assert rep.json() == {"status": "ok"}

def test_api_health():
    rep = client.get("/api/health")
    assert rep.status_code == 200
    assert rep.json() == {"status": "ok"}

def test_metrics():
    rep = client.get("/metrics")
    assert rep.status_code == 200