import pytest
from src.local_db import LocalFileDB


def test_save_and_get(tmp_path):
    dbdir = tmp_path / "data"
    db = LocalFileDB(str(dbdir))
    db.save("test1", {"a": 1})
    assert db.get("test1") == {"a": 1}
    assert "test1" in db.list_keys()


def test_delete(tmp_path):
    dbdir = tmp_path / "data"
    db = LocalFileDB(str(dbdir))
    db.save("todel", [1, 2, 3])
    db.delete("todel")
    with pytest.raises(KeyError):
        db.get("todel")


def test_invalid_key_sanitization(tmp_path):
    db = LocalFileDB(str(tmp_path))
    key = "weird/key\\name:with*chars?"
    db.save(key, "value")
    assert db.get(key) == "value"
