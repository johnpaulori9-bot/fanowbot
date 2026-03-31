# originator.py

import os
import json
from datetime import datetime

WORKFLOW_DIR = os.path.join(os.getcwd(), "workflows")
os.makedirs(WORKFLOW_DIR, exist_ok=True)


class Originator:
    """
    Executes workflow-related commands.
    Creates workflow files and runs them.
    """

    def run_workflow(self, command: str):
        """
        Expected formats:
        - create_workflow name='land management'
        - run_workflow name='land management'
        """

        parts = command.split()
        action = parts[0]

        # Parse key=value pairs
        kwargs = {}
        for item in parts[1:]:
            if "=" in item:
                key, value = item.split("=", 1)
                kwargs[key] = value.strip("'\"")

        if action == "create_workflow":
            return self._create_workflow(kwargs.get("name", "unnamed_workflow"))

        if action == "run_workflow":
            return self._run_existing_workflow(kwargs.get("name"))

        return f"Unknown workflow command: {command}"

    # ---------------------------------------------------------
    # INTERNAL: CREATE WORKFLOW FILE
    # ---------------------------------------------------------
    def _create_workflow(self, name: str):
        workflow = {
            "name": name,
            "created": datetime.utcnow().isoformat() + "Z",
            "steps": [
                "Assess land condition",
                "Identify degradation drivers",
                "Map zones (no-go, reduce-impact, rehabilitation)",
                "Prioritize interventions",
                "Generate final workflow output"
            ]
        }

        file_path = os.path.join(WORKFLOW_DIR, f"{name.replace(' ', '_')}.json")

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(workflow, f, indent=2)

        return f"Workflow '{name}' created at {file_path}"

    # ---------------------------------------------------------
    # INTERNAL: RUN WORKFLOW FILE
    # ---------------------------------------------------------
    def _run_existing_workflow(self, name: str):
        if not name:
            return "No workflow name provided."

        file_path = os.path.join(WORKFLOW_DIR, f"{name.replace(' ', '_')}.json")

        if not os.path.exists(file_path):
            return f"Workflow '{name}' does not exist."

        with open(file_path, "r", encoding="utf-8") as f:
            workflow = json.load(f)

        # Simulate execution
        executed_steps = []
        for step in workflow.get("steps", []):
            executed_steps.append(f"Executed: {step}")

        return {
            "workflow": workflow["name"],
            "executed_steps": executed_steps,
            "status": "completed"
        }
