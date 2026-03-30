# workflows/principle_ingestion_workflow.py

import requests
import uuid
from agents.principle_memory_agent import PrincipleMemoryAgent

class PrincipleIngestionWorkflow:
    """
    Downloads a principle from a URL, extracts text, and stores it.
    """

    def __init__(self):
        self.memory_agent = PrincipleMemoryAgent()

    def run(self, url):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            content = response.text
        except Exception as e:
            return f"Failed to fetch URL: {e}"

        principle = {
            "id": str(uuid.uuid4()),
            "title": self._extract_title(content),
            "content": self._extract_content(content),
            "source_url": url,
        }

        self.memory_agent.add_principle(principle)

        return f"Ingested principle:\nTitle: {principle['title']}\nID: {principle['id']}"

    def _extract_title(self, html):
        # Very simple title extraction
        start = html.find("<title>")
        end = html.find("</title>")
        if start != -1 and end != -1:
            return html[start+7:end].strip()
        return "Untitled Principle"

    def _extract_content(self, html):
        # Extremely simple text extraction
        text = html.replace("<", "\n<")
        return text[:2000]  # keep it small for now
