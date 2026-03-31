import os
import json
from datetime import datetime

from tools import read_file, list_directory, summarize_text, write_file
def build_consult_prompt(query: str):
    return f"Consult prompt: {query}"

class MemoryStore:
    def __init__(self):
        self.data = {}

    def save(self, key, value):
        self.data[key] = value

    def load(self, key):
        return self.data.get(key, None)




# Directory where all generated agents will live
AGENTS_DIR = os.path.join(os.getcwd(), "agents")

# Registry file that tracks all agents
AGENTS_REGISTRY = os.path.join(AGENTS_DIR, "agents.json")


def ensure_agents_registry():
    """
    Ensure that the agents directory and agents.json registry file exist.
    If they don't, create them.
    """
    os.makedirs(AGENTS_DIR, exist_ok=True)

    if not os.path.exists(AGENTS_REGISTRY):
        with open(AGENTS_REGISTRY, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2)


def load_agents_registry():
    """
    Load the agents.json registry and return it as a Python list.
    Ensures the registry exists before loading.
    """
    ensure_agents_registry()

    with open(AGENTS_REGISTRY, "r", encoding="utf-8") as f:
        try:
            agents = json.load(f)
            if not isinstance(agents, list):
                agents = []
        except json.JSONDecodeError:
            agents = []

    return agents


def create_agent(
    name: str,
    purpose: str,
    department: str = "General",
    tier: str = "Standard",
    lineage: str = "Adam(zero)",
):
    """
    Create a new agent file with a full scaffold and register it in agents.json.
    """

    ensure_agents_registry()

    safe_name = "".join(c for c in name if c.isalnum() or c == "_")
    if not safe_name:
        raise ValueError("Agent name must contain at least one alphanumeric character.")

    class_name = safe_name[0].upper() + safe_name[1:]
    file_name = f"{safe_name.lower()}.py"
    file_path = os.path.join(AGENTS_DIR, file_name)

    timestamp = datetime.utcnow().isoformat() + "Z"

    agent_code = f'''"""
Auto‑generated agent: {class_name}
Created: {timestamp}
Purpose: {purpose}
Department: {department}
Tier: {tier}
Lineage: {lineage}
"""

class {class_name}:
    def run(self, query: str):
        return "Agent {class_name} received: " + query
'''

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(agent_code)

    registry = load_agents_registry()
    entry = {
        "name": class_name,
        "file": file_path,
        "purpose": purpose,
        "department": department,
        "tier": tier,
        "lineage": lineage,
        "created": timestamp,
    }
    registry.append(entry)

    with open(AGENTS_REGISTRY, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2)

    return {"file": file_path, "metadata": entry}


# ============================================================
#                  EVERYTHING ADVISOR (ORIGINATOR)
# ============================================================

class EverythingAdvisor:
    """
    The Originator / Everything Advisor.
    Handles:
    - memory recall
    - agent creation
    - file tools
    - LLM reasoning
    """

    def __init__(self, provider):
        self.provider = provider
        self.memory = MemoryStore()

    def run(self, query: str) -> str:
        query = query.strip()

        # --- Tool: read file ---
        if query.startswith("read file "):
            path = query.replace("read file ", "", 1).strip()
            return read_file(path)

        # --- Tool: list directory ---
        if query.startswith("list directory"):
            parts = query.split(" ", 2)
            if len(parts) == 3:
                return list_directory(parts[2])
            return "Usage: list directory <path>"

        # --- Tool: summarize text ---
        if query.startswith("summarize "):
            text = query.replace("summarize ", "", 1).strip()
            return summarize_text(text)

        # --- Tool: write file ---
        if query.startswith("write file "):
            rest = query.replace("write file ", "", 1).strip()
            if "::: " in rest:
                path, content = rest.split("::: ", 1)
                return write_file(path.strip(), content.strip())
            return "Usage: write file <path> ::: <content>"

        # --- Memory: remember ---
        if query.startswith("remember "):
            fact = query.replace("remember ", "", 1).strip()
            self.memory.add("knowledge", {"fact": fact})
            return f"I will remember: {fact}"

        # --- Memory: recall ---
        if query == "recall":
            items = self.memory.get_all()
            if not items:
                return "I have no memories stored."
            return "Here is what I remember:\n" + "\n".join(
                f"- {cat}: {vals}" for cat, vals in items.items()
            )

        # --- Originator: create agent ---
        if query.startswith("create agent "):
            parts = query.split()
            if len(parts) < 3:
                return "Usage: create agent <Name> <purpose>"

            name = parts[2]
            purpose = " ".join(parts[3:]) if len(parts) > 3 else "No purpose provided."

            result = create_agent(
                name=name,
                purpose=purpose,
                department="General",
                tier="Standard",
                lineage="Adam(zero)",
            )

            return (
                f"Created agent '{result['metadata']['name']}'\n"
                f"  File: {result['file']}\n"
                f"  Purpose: {result['metadata']['purpose']}\n"
                f"  Department: {result['metadata']['department']}\n"
                f"  Tier: {result['metadata']['tier']}\n"
                f"  Lineage: {result['metadata']['lineage']}\n"
            )

        # --- Default: LLM reasoning ---
        final_prompt = build_consult_prompt(query, self.memory)
        raw = self.provider.generate(final_prompt)

        # Clean up stop words
        for stop_word in ["You:", "Assistant:"]:
            if stop_word in raw:
                raw = raw.split(stop_word)[0].strip()

        return raw
