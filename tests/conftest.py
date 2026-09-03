import os
import tempfile

os.environ["API_KEY"] = "test-api-key"
os.environ["OPENAI_API_KEY"] = ""
os.environ["MOCK_CRAWLER"] = "true"
os.environ["SCHEDULE_ENABLED"] = "false"

tmp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
tmp_db.close()
db_path = tmp_db.name.replace("\\", "/")
os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def api_headers():
    return {"X-API-Key": "test-api-key"}
