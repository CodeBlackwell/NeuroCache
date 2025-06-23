import os
import shutil
import pytest
from fastapi.testclient import TestClient
from neurocache.main import app
from neurocache.core import vector_store
from neurocache.config import USER_STORES_DIR

client = TestClient(app)

def setup_user_stores(user_ids, dim=8):
    if USER_STORES_DIR.exists():
        shutil.rmtree(USER_STORES_DIR)
    USER_STORES_DIR.mkdir(parents=True, exist_ok=True)
    for user_id in user_ids:
        vector_store.create_index(user_id, dim=dim)

def test_users_endpoint():
    user_ids = ["userA", "userB", "userC"]
    setup_user_stores(user_ids)
    response = client.get("/users")
    assert response.status_code == 200
    data = response.json()["user_ids"]
    assert sorted(data) == sorted(user_ids)

@pytest.fixture(scope="module", autouse=True)
def cleanup():
    yield
    if USER_STORES_DIR.exists():
        shutil.rmtree(USER_STORES_DIR)
