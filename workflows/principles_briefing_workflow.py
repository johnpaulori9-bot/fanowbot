import os
from datetime import datetime
from agents.principle_memory_agent import PrincipleMemoryAgent

class PrinciplesBriefingWorkflow:
    """
    Generates a daily briefing containing one stored principle.
    """

    def __init__(self):
        self.memory_agent = PrincipleMemoryAgent()

    def run(self):
        # 1. Load all stored principles
        principles = self.memory_agent.load_principles()

        if not principles:
            return "No principles stored yet. Use: principle <url>"

        # 2. Pick the next principle (simple rotation)
        principle = principles[0]  # later we can add randomization or indexing

        # 3. Format the briefing
        briefing_text = self._format_briefing(principle)

        # 4. Save to output directory
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)

        filename = f"principle_briefing_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "w") as f:
            f.write(briefing_text)

        return f"Principle briefing generated at: {filepath}"

    def _format_briefing(self, principle):
        """
        Formats a single principle into a readable briefing.
        """

        title = principle.get("title", "Untitled Principle")
        content = principle.get("content", "")
        source = principle.get("source_url", "Unknown source")
        pid = principle.get("id", "N/A")

        return (
            "=== DAILY PRINCIPLE BRIEFING ===\n\n"
            f"Title: {title}\n"
            f"ID: {pid}\n"
            f"Source: {source}\n\n"
            "----- Principle Content -----\n"
            f"{content}\n\n"
            "----- Reflection Prompt -----\n"
            "How can this principle shape one decision you make today?\n"
        )
