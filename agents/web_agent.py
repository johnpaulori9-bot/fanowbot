import requests


class Agent:
    def __init__(self):
        pass

    def fetch_text(self, url: str, timeout: int = 10) -> str:
        """
        Fetches raw text content from a URL.
        Later we can add HTML parsing, extraction, etc.
        """
        print(f"[WebAgent] Fetching URL: {url}")
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
        return resp.text[:8000]  # truncate to avoid huge payloads
