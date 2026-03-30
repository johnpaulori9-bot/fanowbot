from planner import plan
from tools import read_file, list_directory, summarize_text
from advisor import create_agent, load_agents_registry

class AdvisorWorkflow:
    def run(self, advisor, query):
        # Step 1: Planner decides what to do
        decision = plan(query)
        action = decision["action"]
        value = decision["input"]

        # Step 2: Execute the correct action
        if action == "read_file":
            return read_file(value)

        if action == "list_directory":
            return list_directory(value)

        if action == "summarize":
            return summarize_text(advisor.provider, value)

        # --- Originator: create agent ---
        if action == "create_agent":
            name = value.get("name")
            purpose = value.get("purpose", "No purpose provided.")

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

        # Step 3: Default — ask the advisor
        return advisor.run(value)
