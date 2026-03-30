# agent_router.py

from planner import plan
from originator import Originator
from advisor import Agent as AdvisorAgent


def run_agent(agent_name: str, prompt: str):
    """
    Unified interface for all agents.
    agent_name: "planner", "advisor", "originator"
    prompt: user input
    """

    agent_name = agent_name.lower().strip()

    # -----------------------------
    # PLANNER (function-based agent)
    # -----------------------------
    if agent_name == "planner":
        return plan(prompt)

    # -----------------------------
    # ADVISOR (class with act())
    # -----------------------------
    if agent_name == "advisor":
        advisor = AdvisorAgent()
        return advisor.act(prompt)

    # -----------------------------
    # ORIGINATOR (workflow executor)
    # -----------------------------
    if agent_name == "originator":
        originator = Originator()

        # Expecting prompt like: "workflow_name param1=value param2=value"
        parts = prompt.split()
        workflow_name = parts[0]
        kwargs = {}

        # Parse key=value pairs
        for item in parts[1:]:
            if "=" in item:
                key, value = item.split("=", 1)
                kwargs[key] = value

        return originator.run_workflow(workflow_name, **kwargs)

    # -----------------------------
    # UNKNOWN AGENT
    # -----------------------------
    return f"Unknown agent: {agent_name}"
