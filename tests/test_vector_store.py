import os
import shutil
import numpy as np
import pytest
from neurocache.core import vector_store

def setup_user_store(user_id):
    # Remove any existing store for a clean test
    dir_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'user_stores')
    index_path = os.path.join(dir_path, f"{user_id}.index")
    meta_path = os.path.join(dir_path, f"{user_id}_meta.json")
    if os.path.exists(index_path):
        os.remove(index_path)
    if os.path.exists(meta_path):
        os.remove(meta_path)
    os.makedirs(dir_path, exist_ok=True)

def test_create_index_and_add_embeddings():
    user_id = "testuser"
    setup_user_store(user_id)
    dim = 8
    # Create index
    index = vector_store.create_index(user_id, dim=dim)
    assert index.d == dim
    # Add embeddings
    embeddings = np.eye(dim, dtype=np.float32).tolist()  # 8 identity vectors
    metadatas = [{"source": "unit_test", "chunk_position": i} for i in range(dim)]
    vector_store.add_embeddings(user_id, embeddings, metadatas)
    # Index should now have 8 vectors
    index2 = vector_store.create_index(user_id, dim=dim)
    assert index2.ntotal == dim
    # Metadata file should have 8 items
    meta_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'user_stores', f"{user_id}_meta.json")
    with open(meta_path) as f:
        meta = f.read()
    assert meta.count('unit_test') == dim

def test_query_index():
    user_id = "testuser"
    dim = 8
    # Query for the first vector
    query_vec = np.eye(dim, dtype=np.float32)[0].tolist()
    results = vector_store.query_index(user_id, query_vec, top_k=3)
    assert len(results) == 3
    assert results[0]["chunk_position"] == 0
    assert results[0]["score"] < results[1]["score"]

@pytest.fixture(scope="module", autouse=True)
def cleanup():
    # Clean up after tests
    yield
    dir_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'user_stores')
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
