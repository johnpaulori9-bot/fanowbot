# workflows/design_review_workflow.py

import os
from datetime import datetime
from agents.principle_memory_agent import PrincipleMemoryAgent

class DesignReviewWorkflow:
    """
    Evaluates the system design against stored principles.
    """

    def __init__(self):
        self.memory_agent = PrincipleMemoryAgent()

    def run(self):
        # Load principles
        principles = self.memory_agent.load_principles()

        if not principles:
            return "No principles stored yet. Use: principle <url>"

        # Load system description
        system_description = self._load_system_description()

        # Generate review
        review_text = self._generate_review(system_description, principles)

        # Save output
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)

        filename = f"design_review_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "w") as f:
            f.write(review_text)

        return f"Design review generated at: {filepath}"

    def _load_system_description(self):
        """
        Loads the system description from project_prompt.txt.
        """
        try:
            with open("project_prompt.txt", "r") as f:
                return f.read()
        except FileNotFoundError:
            return "System description not found (project_prompt.txt missing)."

    def _generate_review(self, system_description, principles):
        """
        Compares each principle against the system description.
        """

        header = (
            "=== SYSTEM DESIGN REVIEW ===\n\n"
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            "----- System Description -----\n"
            f"{system_description}\n\n"
            "----- Principle-by-Principle Review -----\n\n"
        )

        body = ""

        for p in principles:
            title = p.get("title", "Untitled Principle")
            content = p.get("content", "")
            pid = p.get("id", "N/A")

            body += (
                f"### Principle: {title}\n"
                f"ID: {pid}\n\n"
                f"Content:\n{content}\n\n"
                "Assessment:\n"
                f"- Alignment: Does the system follow this principle?\n"
                f"- Gaps: Where does the system fall short?\n"
                f"- Opportunities: How can the system better embody this principle?\n\n"
                "----------------------------------------\n\n"
            )

        return header + body
