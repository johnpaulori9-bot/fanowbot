import json
import os
from datetime import datetime


class TextExtractor:
    """
    Extracts raw and cleaned text from files and stores them in text_memory.json.
    """

    def __init__(self, path: str = "memory/text_memory.json"):
        # Path to the JSON file where we store text memory
        self.path = path
        # Load existing data from disk (or start empty)
        self._data = self._load()

    # -------------------------
    # Load/save helpers
    # -------------------------

    def _load(self):
        """
        Load text_memory.json from disk.
        If it doesn't exist or is invalid, return an empty dict.
        """
        if not os.path.exists(self.path):
            return {}
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def _save(self):
        """
        Save current in-memory data back to text_memory.json.
        """
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2)

    def _now(self):
        """
        Return current UTC time as an ISO string.
        """
        return datetime.utcnow().isoformat()

    # -------------------------
    # Extraction methods
    # -------------------------

    def _extract_plain(self, file_path):
        """
        Extract text from a plain text file (.txt or similar).
        """
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()

        # For now, we treat the whole file as one "page"
        pages = [{"page_number": 1, "text": text}]
        tables = []
        return text, pages, tables

    def _extract_pdf_placeholder(self, file_path):
        """
        Placeholder for PDF extraction.
        Later you can plug in a real PDF library.
        """
        return "", [], []

    def _extract_docx_placeholder(self, file_path):
        """
        Placeholder for Word (.docx) extraction.
        """
        return "", [], []

    def _extract_image_placeholder(self, file_path):
        """
        Placeholder for image OCR extraction.
        """
        return "", [], []

    # -------------------------
    # Public API
    # -------------------------

    def rebuild_text_memory(self, file_id, file_path):
        """
        Main method called by MemoryAgent.

        - Checks the file exists
        - Chooses an extraction method based on extension
        - Stores the result in text_memory.json under file_id
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        ext = file_path.lower().split(".")[-1]

        if ext == "txt":
            raw_text, pages, tables = self._extract_plain(file_path)
        elif ext == "pdf":
            raw_text, pages, tables = self._extract_pdf_placeholder(file_path)
        elif ext == "docx":
            raw_text, pages, tables = self._extract_docx_placeholder(file_path)
        elif ext in ["jpg", "jpeg", "png"]:
            raw_text, pages, tables = self._extract_image_placeholder(file_path)
        else:
            # Fallback: try to read as plain text
            raw_text, pages, tables = self._extract_plain(file_path)

        clean_text = raw_text.strip()

        # Store/update the record for this file_id
        self._data[file_id] = {
            "file_id": file_id,
            "raw_text": raw_text,
            "clean_text": clean_text,
            "sections": [],
            "pages": pages,
            "tables": tables,
            "last_extracted": self._now()
        }

        # Save everything back to disk
        self._save()

    def get_text_memory(self, file_id):
        """
        Retrieve the stored text memory for a given file_id.
        """
        return self._data.get(file_id)
