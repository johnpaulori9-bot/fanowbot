# agent_router.py

from planner import Planner
from originator import Originator
from advisor import Advisor

def run_agent(agent_name: str, prompt: str) -> str:
    """
    Routes a request to the correct agent.
    Returns the agent's output as a string.
    """

    agent_name = agent_name.lower().strip()

    if agent_name == "planner":
        agent = Planner()
        return agent.run(prompt)

    if agent_name == "originator":
        agent = Originator()
        return agent.run(prompt)

    if agent_name == "advisor":
        agent = Advisor()
        return agent.run(prompt)

    return f"Unknown agent: {agent_name}"
