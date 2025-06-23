# NeuroCache Blog Notes

A living document for development insights, debugging, design decisions, and milestones—structured for future blogging.

---

## Chronological Log

### 2025-06-22
- **Scaffolded FastAPI project:** Created main app, core modules (`ingestion.py`, `vector_store.py`), and Pydantic models.
- **Testing Framework:** Set up pytest and wrote initial unit tests for ingestion and chunking.
- **Implemented Ingestion Pipeline:** File/URL loading, chunking, and metadata augmentation.
- **Dependency Management:** Resolved `fastapi`/`pydantic` version conflicts by removing strict pins.

---

## Debugging & Solutions

- **Dependency Conflict:**
  - *Problem:* `fastapi==0.95.2` and `pydantic==2.1.1` were incompatible.
  - *Solution:* Removed version pins, let pip resolve compatible versions. Installation succeeded.
- **Git Push Error:**
  - *Problem:* `git push` failed due to no committed files after repo init.
  - *Solution:* Created and committed project skeleton, then push succeeded.

---

## Design Decisions

- **File Structure:**
  - Adopted a modular structure: `neurocache/` for app logic, `data/` for persistent artifacts, `tests/` for all test code.
- **Testing Policy:**
  - Added a rule to always write unit tests for every completed feature.
- **Blog Notes Structure:**
  - This document now explicitly tracks debugging, design, and milestone events for transparency and future blogging.
- **Color Commentary:** For blog posts, I'll write a narrative around the listed events, adding insights, feelings, and lessons learned.

---

## Future Plans

- **Vector Store:** Implement FAISS index creation and storage.
- **Query Endpoint:** Accept `user_id`, `question`, `top_k`, and optional `metadata_filters`.
- **Users Endpoint:** Implement a way to track created vector stores.
- **Management & Showcase Endpoints:** Implement `/delete_source` and `/sources/{user_id}`.

---

## Add new entries below
