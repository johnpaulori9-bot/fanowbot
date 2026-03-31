# planner.py
"""
Multi‑step Planner for Orchestrator Mode (Option D)
This planner breaks user requests into structured steps
and assigns each step to the correct agent.
"""

def plan(query: str):
    q = query.lower().strip()

    # ---------------------------------------------------------
    # 1. CREATE WORKFLOW REQUESTS
    # ---------------------------------------------------------
    if "create a workflow for" in q or "workflow for" in q:
        # Extract workflow name
        workflow_name = (
            q.replace("create a workflow for", "")
             .replace("workflow for", "")
             .strip()
        )

        if not workflow_name:
            workflow_name = "unnamed_workflow"

        # Multi‑step orchestrator plan
        return {
            "steps": [
                {
                    "agent": "advisor",
                    "input": f"analyze the domain and requirements for {workflow_name}"
                },
                {
                    "agent": "advisor",
                    "input": f"identify the components needed for a {workflow_name} workflow"
                },
                {
                    "agent": "originator",
                    "input": f"create_workflow name='{workflow_name}'"
                }
            ]
        }

    # ---------------------------------------------------------
    # 2. CREATE AGENT COMMAND
    # ---------------------------------------------------------
    if q.startswith("create agent "):
        parts = q.split()
        if len(parts) >= 3:
            name = parts[2]
            purpose = " ".join(parts[3:]) if len(parts) > 3 else "No purpose provided."
            return {
                "steps": [
                    {
                        "agent": "originator",
                        "input": f"create_agent name='{name}' purpose='{purpose}'"
                    }
                ]
            }

    # ---------------------------------------------------------
    # 3. TOOL COMMANDS
    # ---------------------------------------------------------
    if q.startswith("read file "):
        return {
            "steps": [
                {"agent": "originator", "input": f"read_file path='{q.replace('read file ', '').strip()}'"}
            ]
        }

    if q.startswith("list directory "):
        return {
            "steps": [
                {"agent": "originator", "input": f"list_directory path='{q.replace('list directory ', '').strip()}'"}
            ]
        }

    if q.startswith("summarize "):
        return {
            "steps": [
                {"agent": "advisor", "input": f"summarize this: {q.replace('summarize ', '').strip()}"}
            ]
        }

    # ---------------------------------------------------------
    # 4. DEFAULT FALLBACK
    # ---------------------------------------------------------
    return {
        "steps": [
            {"agent": "advisor", "input": query}
        ]
    }
