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

        # Legacy single-step format
        if isinstance(plan_output, dict) and "action" in plan_output:
            return _execute_single_step(plan_output["action"], plan_output["input"])

        # Multi-step format
        if isinstance(plan_output, dict) and "steps" in plan_output:
            results = []
            for step in plan_output["steps"]:
                agent = step.get("agent")
                input_data = step.get("input", "")
                step_result = _execute_single_step(agent, input_data)
                results.append(
                    {
                        "agent": agent,
                        "input": input_data,
                        "output": step_result,
                    }
                )
            return results

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
    if not agent:
        return "No agent specified in step."

    agent = agent.lower().strip()

    if agent == "advisor":
        advisor = AdvisorAgent()
        return advisor.act(input_data)

    if agent == "originator":
        originator = Originator()
        return originator.run_workflow(input_data)

    return f"Unknown agent in plan: {agent}"
