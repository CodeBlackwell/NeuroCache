"""
Module: config.py
Centralized configuration and path management.
"""
import os
from pathlib import Path

# Base directories
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# User stores
USER_STORES_DIR = DATA_DIR / "user_stores"

# Temporary storage
TEMP_UPLOADS_DIR = DATA_DIR / "temp_uploads"

# Document storage
DOCUMENTS_DIR = DATA_DIR / "documents"

def ensure_dirs_exist():
    """Ensure all required directories exist."""
    USER_STORES_DIR.mkdir(parents=True, exist_ok=True)
    TEMP_UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)

# Create directories on import
ensure_dirs_exist()
