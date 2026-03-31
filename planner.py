# planner.py
"""
Multi-step planner for orchestrator mode.

Given a natural language query, returns a plan as:
    {"steps": [ { "agent": "...", "input": "..." }, ... ]}
"""

def plan(query: str):
    q = query.lower().strip()

    # ---------------------------------------------------------
    # 1. CREATE WORKFLOW REQUESTS
    # ---------------------------------------------------------
    if "create a workflow for" in q or "workflow for" in q:
        workflow_name = q
        for marker in ["create a workflow for", "workflow for"]:
            if marker in workflow_name:
                workflow_name = workflow_name.split(marker, 1)[1].strip()
        if not workflow_name:
            workflow_name = "unnamed_workflow"

        return {
            "steps": [
                {
                    "agent": "advisor",
                    "input": f"Analyze the domain and requirements for '{workflow_name}'."
                },
                {
                    "agent": "advisor",
                    "input": f"Identify the components needed for a '{workflow_name}' workflow."
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
    # 3. TOOL-LIKE COMMANDS
    # ---------------------------------------------------------
    if q.startswith("read file "):
        path = q.replace("read file ", "", 1).strip()
        return {
            "steps": [
                {"agent": "originator", "input": f"read_file path='{path}'"}
            ]
        }

    if q.startswith("list directory "):
        path = q.replace("list directory ", "", 1).strip()
        return {
            "steps": [
                {"agent": "originator", "input": f"list_directory path='{path}'"}
            ]
        }

    if q.startswith("summarize "):
        text = q.replace("summarize ", "", 1).strip()
        return {
            "steps": [
                {"agent": "advisor", "input": f"Summarize this: {text}"}
            ]
        }

    # ---------------------------------------------------------
    # 4. DEFAULT FALLBACK → ADVISOR
    # ---------------------------------------------------------
    return {
        "steps": [
            {"agent": "advisor", "input": query}
        ]
    }
