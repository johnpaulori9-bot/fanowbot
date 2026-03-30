# agents/principle_memory_agent.py

import json
import os

class PrincipleMemoryAgent:
    """
    Stores and retrieves principles from principles.json.
    """

    def __init__(self, filename="principles.json"):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump([], f)

    def load_principles(self):
        with open(self.filename, "r") as f:
            return json.load(f)

    def save_principles(self, principles):
        with open(self.filename, "w") as f:
            json.dump(principles, f, indent=4)

    def add_principle(self, principle):
        principles = self.load_principles()
        principles.append(principle)
        self.save_principles(principles)

