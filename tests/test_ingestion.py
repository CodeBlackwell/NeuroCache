import os
import uuid
import pytest
from neurocache.core.ingestion import load_document, chunk_and_augment


def test_load_document_txt(tmp_path):
    # Create a temporary text file
    file_path = tmp_path / "sample.txt"
    sample_text = "Hello, NeuroCache!"
    file_path.write_text(sample_text)

    # Load document
    content = load_document(file_path=str(file_path))
    assert sample_text in content


def test_pdf_ingestion():
    pdf_path = os.path.abspath("data/documents/RepromptAI_CCR.pdf")
    if not os.path.exists(pdf_path):
        pytest.skip("Test PDF not found: " + pdf_path)
    content = load_document(file_path=pdf_path)
    assert isinstance(content, str)
    assert len(content) > 100  # Should be non-trivial length
    chunks = chunk_and_augment(content, {"source": pdf_path})
    assert isinstance(chunks, list)
    assert len(chunks) > 1
    for i, chunk in enumerate(chunks):
        assert "text" in chunk
        assert "metadata" in chunk
        assert chunk["metadata"]["source"] == pdf_path
        assert chunk["metadata"]["chunk_position"] == i

def test_chunk_and_augment_simple():
    text = "This is a test." * 200  # long text to trigger splitting
    metadata = {"source": "test"}

    chunks = chunk_and_augment(text, metadata)
    assert isinstance(chunks, list)
    assert len(chunks) > 1
    # Each chunk should have text and metadata with correct keys
    for i, chunk in enumerate(chunks):
        assert "text" in chunk
        assert "metadata" in chunk
        assert chunk["metadata"]["source"] == "test"
        assert chunk["metadata"]["chunk_position"] == i
