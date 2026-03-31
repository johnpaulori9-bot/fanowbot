import os
import json
from datetime import datetime

# -----------------------------
# Local safe replacements
# -----------------------------

def build_consult_prompt(query: str):
    return f"Consult prompt: {query}"

class MemoryStore:
    def __init__(self):
        self.data = {}

    def save(self, key, value):
        self.data[key] = value

    def load(self, key):
        return self.data.get(key)


# -----------------------------
# Agent registry system
# -----------------------------

AGENTS_DIR = os.path.join(os.getcwd(), "agents")
AGENTS_REGISTRY = os.path.join(AGENTS_DIR, "agents.json")


def ensure_agents_registry():
    os.makedirs(AGENTS_DIR, exist_ok=True)

    if not os.path.exists(AGENTS_REGISTRY):
        with open(AGENTS_REGISTRY, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2)


def load_agents_registry():
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


# -----------------------------
# Advisor Agent (required)
# -----------------------------

class Agent:
    def act(self, query: str):
        return f"Advisor received: {query}"
