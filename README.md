# AI_Test - local file DB test project

This repository contains a minimal Python module that implements a small local file-based key-value store and unit tests to validate it.

Files created:

- `src/local_db.py` - LocalFileDB implementation (JSON files per key).
- `tests/test_local_db.py` - pytest unit tests covering save/get/delete and key sanitization.
- `requirements.txt` - test dependencies (pytest)

How to run tests (PowerShell on Windows):

```powershell
python -m pip install -r requirements.txt
python -m pytest -q
```

Notes:
- The DB stores one JSON file per key under the provided data directory.
- Keys are preserved in the file payload so `list_keys()` returns original keys.

Next steps you might try:
- Add a small CLI or REST API wrapper around the DB.
- Add concurrency tests or file-locking for multi-process safety.
