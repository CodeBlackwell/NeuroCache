import os
import shutil
import pytest
from fastapi.testclient import TestClient
from neurocache.main import app
from neurocache.core import vector_store
import numpy as np

client = TestClient(app)

def setup_user_store(user_id):
    dir_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'user_stores')
    index_path = os.path.join(dir_path, f"{user_id}.index")
    meta_path = os.path.join(dir_path, f"{user_id}_meta.json")
    if os.path.exists(index_path):
        os.remove(index_path)
    if os.path.exists(meta_path):
        os.remove(meta_path)
    os.makedirs(dir_path, exist_ok=True)

def test_query_endpoint():
    user_id = "testuser_query"
    setup_user_store(user_id)
    dim = 8
    # Add known embeddings and metadata
    embeddings = np.eye(dim, dtype=np.float32).tolist()
    metadatas = [{"source": "integration_test", "chunk_position": i, "tag": "even" if i % 2 == 0 else "odd"} for i in range(dim)]
    vector_store.add_embeddings(user_id, embeddings, metadatas)
    # Query for the first vector
    query_vec = np.eye(dim, dtype=np.float32)[0].tolist()
    # Monkeypatch OpenAIEmbeddings to return our query_vec for test
    import neurocache.main as main_mod
    class DummyEmbed:
        def embed_query(self, q):
            return query_vec
    main_mod.OpenAIEmbeddings = DummyEmbed
    # Make POST request to /query
    payload = {
        "user_id": user_id,
        "question": "irrelevant for test",
        "top_k": 3,
        "metadata_filters": {"tag": "even"}
    }
    response = client.post("/query", json=payload)
    assert response.status_code == 200
    data = response.json()["results"]
    assert len(data) >= 1
    # Should only return chunks with tag 'even'
    for r in data:
        assert r["tag"] == "even"
    assert data[0]["chunk_position"] == 0

@pytest.fixture(scope="module", autouse=True)
def cleanup():
    yield
    dir_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'user_stores')
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
