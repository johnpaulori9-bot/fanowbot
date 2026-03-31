# agent_router.py

from planner import plan
from originator import Originator
from advisor import Agent as AdvisorAgent


def run_agent(agent_name: str, prompt: str):
    """
    Unified interface for all agents.
    Supports multi-step orchestrator plans.
    """

    agent_name = agent_name.lower().strip()

    # ---------------------------------------------------------
    # 1. PLANNER — may return multi-step plan
    # ---------------------------------------------------------
    if agent_name == "planner":
        plan_output = plan(prompt)

        # If planner returns a single-step dict
        if "action" in plan_output:
            return _execute_single_step(plan_output["action"], plan_output["input"])

        # If planner returns a multi-step plan
        if "steps" in plan_output:
            result = None
            for step in plan_output["steps"]:
                agent = step["agent"]
                input_data = step["input"]
                result = _execute_single_step(agent, input_data)
            return result

        return "Planner returned an invalid plan format."

    # ---------------------------------------------------------
    # 2. DIRECT CALLS TO ADVISOR
    # ---------------------------------------------------------
    if agent_name == "advisor":
        advisor = AdvisorAgent()
        return advisor.act(prompt)

    # ---------------------------------------------------------
    # 3. DIRECT CALLS TO ORIGINATOR
    # ---------------------------------------------------------
    if agent_name == "originator":
        originator = Originator()
        return originator.run_workflow(prompt)

    # ---------------------------------------------------------
    # 4. UNKNOWN AGENT
    # ---------------------------------------------------------
    return f"Unknown agent: {agent_name}"


# ---------------------------------------------------------
# INTERNAL HELPER — executes a single step
# ---------------------------------------------------------
def _execute_single_step(agent: str, input_data: str):
    agent = agent.lower().strip()

    if agent == "advisor":
        advisor = AdvisorAgent()
        return advisor.act(input_data)

    if agent == "originator":
        originator = Originator()
        return originator.run_workflow(input_data)

    return f"Unknown agent in plan: {agent}"
