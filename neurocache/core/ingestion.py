"""
Module: ingestion.py
Handles document loading, chunking, and metadata augmentation.
"""
import os
from typing import Optional, Dict, List
from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredFileLoader, WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def load_document(file_path: Optional[str] = None, url: Optional[str] = None) -> str:
    """
    Load raw text from a local file or a URL.
    """
    if url:
        loader = WebBaseLoader(url)
        docs = loader.load()
    elif file_path:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            loader = PyPDFLoader(file_path)
        else:
            loader = TextLoader(file_path)
        docs = loader.load()
    else:
        return ""
    text = "\n\n".join([doc.page_content for doc in docs])
    return text


def chunk_and_augment(text: str, metadata: Dict) -> List[Dict]:
    """
    Break text into chunks and attach metadata (source, position, tags).
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = splitter.split_text(text)
    chunks = []
    for i, chunk in enumerate(texts):
        md = metadata.copy()
        md["chunk_position"] = i
        chunks.append({"text": chunk, "metadata": md})
    return chunks
