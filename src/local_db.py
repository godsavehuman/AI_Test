import os
import json
import hashlib
from typing import Any, List


class LocalFileDB:
    """A tiny file-based local key->JSON-value store.

    Implementation notes:
    - Each key is stored as a separate JSON file under the provided root directory.
    - Keys are sanitized into filenames; if the key sanitizes to empty, we use a sha256 hash.
    - Stored payload contains the original key and the data to preserve mapping.
    - Methods: save(key, data), get(key), delete(key), list_keys().
    """

    def __init__(self, root: str = None):
        # Default data directory is ../data relative to this file
        if root is None:
            root = os.path.join(os.path.dirname(__file__), "..", "data")
        self.root = os.path.abspath(root)
        os.makedirs(self.root, exist_ok=True)

    def _filename(self, key: str) -> str:
        # Sanitize key to a filesystem-safe name; keep alnum, -_. else replace
        safe = ''.join(c if (c.isalnum() or c in '-_.') else '_' for c in key)
        if not safe:
            # fall back to hash if sanitization produced empty string
            safe = hashlib.sha256(key.encode('utf-8')).hexdigest()
        return os.path.join(self.root, f"{safe}.json")

    def save(self, key: str, data: Any) -> None:
        """Persist data under key. Overwrites existing record for the same key."""
        path = self._filename(key)
        payload = {"key": key, "data": data}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

    def get(self, key: str) -> Any:
        """Retrieve data for key. Raises KeyError if not found."""
        path = self._filename(key)
        if not os.path.exists(path):
            raise KeyError(f"Key not found: {key}")
        with open(path, "r", encoding="utf-8") as f:
            payload = json.load(f)
            return payload.get("data")

    def delete(self, key: str) -> None:
        """Delete a record by key. Raises KeyError if not found."""
        path = self._filename(key)
        if os.path.exists(path):
            os.remove(path)
        else:
            raise KeyError(f"Key not found: {key}")

    def list_keys(self) -> List[str]:
        """Return a list of stored keys (original keys preserved in files)."""
        keys: List[str] = []
        for fname in os.listdir(self.root):
            if not fname.endswith('.json'):
                continue
            try:
                with open(os.path.join(self.root, fname), "r", encoding="utf-8") as f:
                    payload = json.load(f)
                    if "key" in payload:
                        keys.append(payload["key"])
            except Exception:
                # If a file is malformed, skip it to keep listing robust
                continue
        return keys
