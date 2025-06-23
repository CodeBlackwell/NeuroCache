"""
Module: vector_store.py
Manages embedding generation and FAISS index operations.
"""
import os
import json
import numpy as np
import faiss
from typing import List, Dict
from neurocache.config import USER_STORES_DIR


def _get_index_path(user_id: str):
    return USER_STORES_DIR / f"{user_id}.index"

def _get_meta_path(user_id: str):
    return USER_STORES_DIR / f"{user_id}_meta.json"


def create_index(user_id: str, dim: int = 1536):
    """
    Initialize or load a FAISS index for a user. Default dim=1536 for OpenAI embeddings.
    """
    USER_STORES_DIR.mkdir(parents=True, exist_ok=True)
    index_path = _get_index_path(user_id)
    if os.path.exists(index_path):
        return faiss.read_index(str(index_path))
    index = faiss.IndexFlatL2(dim)
    faiss.write_index(index, str(index_path))
    # Initialize empty metadata
    with open(_get_meta_path(user_id), "w") as f:
        json.dump([], f)
    return index


def add_embeddings(user_id: str, embeddings: List[List[float]], metadatas: List[Dict]):
    """
    Add embeddings and metadata to the user's FAISS index.
    """
    index_path = _get_index_path(user_id)
    meta_path = _get_meta_path(user_id)
    if os.path.exists(index_path):
        index = faiss.read_index(str(index_path))
    else:
        index = create_index(user_id, dim=len(embeddings[0]))
    arr = np.array(embeddings).astype('float32')
    index.add(arr)
    faiss.write_index(index, str(index_path))
    # Append metadata
    if os.path.exists(meta_path):
        with open(str(meta_path), "r") as f:
            meta = json.load(f)
    else:
        meta = []
    meta.extend(metadatas)
    with open(str(meta_path), "w") as f:
        json.dump(meta, f)


def query_index(user_id: str, query_embedding: List[float], top_k: int):
    """
    Query the user's FAISS index and return top_k results with metadata.
    """
    index_path = _get_index_path(user_id)
    meta_path = _get_meta_path(user_id)
    if not os.path.exists(index_path) or not os.path.exists(meta_path):
        return []
    index = faiss.read_index(str(index_path))
    with open(str(meta_path), "r") as f:
        meta = json.load(f)
    arr = np.array([query_embedding]).astype('float32')
    D, I = index.search(arr, top_k)
    results = []
    for idx, dist in zip(I[0], D[0]):
        if idx < 0 or idx >= len(meta):
            continue
        item = meta[idx].copy()
        item['score'] = float(dist)
        results.append(item)
    return results
