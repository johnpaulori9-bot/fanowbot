import re
from typing import Optional

import requests
from bs4 import BeautifulSoup


class Agent:
    """
    ReadabilityAgent

    Fetches a URL and extracts the main readable article content.
    """

    def __init__(self, timeout: int = 15):
        self.timeout = timeout

    def fetch_html(self, url: str) -> Optional[str]:
        try:
            resp = requests.get(url, timeout=self.timeout)
            resp.raise_for_status()
            return resp.text
        except Exception as e:
            print(f"[ReadabilityAgent] Error fetching URL {url}: {e}")
            return None

    def extract_main_text(self, html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")

        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        article = soup.find("article")
        if article:
            text = article.get_text(separator="\n")
        else:
            candidates = []
            for tag_name in ["main", "section", "div"]:
                for el in soup.find_all(tag_name):
                    text = el.get_text(separator="\n").strip()
                    if len(text.split()) > 100:
                        candidates.append(text)
            if candidates:
                text = max(candidates, key=len)
            else:
                body = soup.body or soup
                text = body.get_text(separator="\n")

        text = re.sub(r"\s+\n", "\n", text)
        text = re.sub(r"\n\s+", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    def read_url(self, url: str) -> Optional[str]:
        html = self.fetch_html(url)
        if not html:
            return None
        return self.extract_main_text(html)
