import os
import tempfile

os.environ["SOCIAL_AI_API_KEY"] = "test-api-key"
os.environ["SOCIAL_AI_LLM_API_KEY"] = ""
os.environ["SOCIAL_AI_MOCK_CRAWLER"] = "true"
os.environ["SOCIAL_AI_SCHEDULE_ENABLED"] = "false"

tmp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
tmp_db.close()
db_path = tmp_db.name.replace("\\", "/")
os.environ["SOCIAL_AI_DATABASE_URL"] = f"sqlite:///{db_path}"

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
