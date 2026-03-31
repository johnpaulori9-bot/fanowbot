# originator.py

import os
import json
import shlex
from datetime import datetime

# Directory for workflow files
WORKFLOW_DIR = os.path.join(os.getcwd(), "workflow")
os.makedirs(WORKFLOW_DIR, exist_ok=True)


class Originator:
    """
    Executes workflow-related commands.
    Creates and runs workflow files.
    """

    def run_workflow(self, command: str):
        """
        Accepts commands like:
        - create_workflow name='land management'
        - run_workflow name='land management'
        """

        if not command:
            return "Empty workflow command."

        # Use shlex to preserve quoted strings
        parts = shlex.split(command)
        action = parts[0]

        # Parse key=value parameters
        params = {}
        for item in parts[1:]:
            if "=" in item:
                key, value = item.split("=", 1)
                params[key] = value.strip("'").strip('"')

        if action == "create_workflow":
            return self._create_workflow(params)

        if action == "run_workflow":
            return self._run_existing_workflow(params)

        return f"Unknown workflow command: {command}"

    # ---------------------------------------------------------
    # CREATE WORKFLOW FILE
    # ---------------------------------------------------------
    def _create_workflow(self, params):
        name = params.get("name", "unnamed_workflow")
        safe_name = name.replace(" ", "_")
        file_path = os.path.join(WORKFLOW_DIR, f"{safe_name}.json")

        workflow = {
            "name": name,
            "safe_name": safe_name,
            "created": datetime.utcnow().isoformat() + "Z",
            "steps": [
                "Assess land condition",
                "Identify degradation drivers",
                "Map zones (no-go, reduce-impact, rehabilitation)",
                "Prioritize interventions",
                "Generate final workflow output"
            ],
            "status": "created"
        }

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(workflow, f, indent=2)

        return f"Workflow '{name}' created at {file_path}"

    # ---------------------------------------------------------
    # RUN EXISTING WORKFLOW
    # ---------------------------------------------------------
    def _run_existing_workflow(self, params):
        name = params.get("name")
        if not name:
            return "No workflow name provided."

        safe_name = name.replace(" ", "_")
        file_path = os.path.join(WORKFLOW_DIR, f"{safe_name}.json")

        if not os.path.exists(file_path):
            return f"Workflow '{name}' does not exist."

        with open(file_path, "r", encoding="utf-8") as f:
            workflow = json.load(f)

        executed_steps = []
        for step in workflow.get("steps", []):
            executed_steps.append(f"Executed: {step}")

        return {
            "workflow": workflow.get("name", name),
            "file": file_path,
            "executed_steps": executed_steps,
            "status": "completed"
        }
