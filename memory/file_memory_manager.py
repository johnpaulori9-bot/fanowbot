import json
import os
import hashlib
from datetime import datetime


class FileMemoryManager:
    """
    Tracks files, their IDs, hashes, and versions.
    Stores everything in file_memory.json.
    """

    def __init__(self, path="memory/file_memory.json"):
        self.path = path
        self._data = self._load()

    def _load(self):
        if not os.path.exists(self.path):
            return {}
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}

    def _save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2)

    def _hash_file(self, file_path):
        """
        Create a SHA256 hash of the file contents.
        """
        sha = hashlib.sha256()
        with open(file_path, "rb") as f:
            sha.update(f.read())
        return sha.hexdigest()

    def update_file_record(self, file_path):
        """
        Main method called by MemoryAgent.

        - Computes file hash
        - Checks if file already exists
        - Assigns file_id if new
        - Increments version if changed
        """
        file_hash = self._hash_file(file_path)

        # Check if file already exists
        for file_id, record in self._data.items():
            if record["path"] == file_path:
                # Existing file
                if record["hash"] == file_hash:
                    # No change
                    return file_id, False, record["version"]

                # File changed → new version
                old_version = record["version"]
                new_version = old_version + 1

                self._data[file_id]["hash"] = file_hash
                self._data[file_id]["version"] = new_version
                self._data[file_id]["last_updated"] = datetime.utcnow().isoformat()

                self._save()
                return file_id, True, old_version

        # New file → create new file_id
        file_id = f"file-{len(self._data) + 1}"

        self._data[file_id] = {
            "file_id": file_id,
            "path": file_path,
            "hash": file_hash,
            "version": 1,
            "created": datetime.utcnow().isoformat(),
            "last_updated": datetime.utcnow().isoformat()
        }

        self._save()
        return file_id, True, None
