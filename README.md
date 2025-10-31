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

LLM / automation: run tests and produce machine-readable output

If you want an LLM or automation to both run and read the test results, produce a machine-readable report (JUnit XML) that can be parsed programmatically. From PowerShell run:

```powershell
# run all tests and write JUnit XML to results.xml (recommended for tooling/LLMs)
python -m pytest --maxfail=1 -q --junitxml=results.xml

# show the XML report content so a reader/agent can parse it
Get-Content results.xml -Raw
```

To run only the single test module in this repo and produce the same XML report:

```powershell
python -m pytest tests/test_local_db.py --maxfail=1 -q --junitxml=results.xml
Get-Content results.xml -Raw
```

Notes and optional tooling:
- `--junitxml` is built into pytest and requires no extra plugins; XML is well-suited for programmatic parsing.
- If you prefer JSON output, you can install a plugin such as `pytest-json-report` and run `pytest --json-report --json-report-file=results.json` (not included in `requirements.txt` by default).

Notes:
- The DB stores one JSON file per key under the provided data directory.
- Keys are preserved in the file payload so `list_keys()` returns original keys.

Next steps you might try:
- Add a small CLI or REST API wrapper around the DB.
- Add concurrency tests or file-locking for multi-process safety.
