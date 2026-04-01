# finance_router.py
"""
Financial router for orchestrator mode.

This module coordinates:
- finance_planner.plan(...)
- POSBot
- AccountingBot

It mirrors your main agent_router pattern, but is scoped to financial flows.
"""

from typing import Any, Dict, List, Union

from finance_planner import plan
from bots.pos_bot import POSBot
from bots.accounting_bot import AccountingBot


def run_finance_agent(agent_name: str, prompt: str) -> Union[str, Dict[str, Any], List[Dict[str, Any]]]:
    """
    Unified interface for financial agents.

    Supports:
    - "finance_planner" / "finance" → multi-step planning and execution
    - "pos" → direct POS bot calls
    - "accounting" → direct accounting bot calls
    """

    agent_name = agent_name.lower().strip()

    # ---------------------------------------------------------
    # 1. FINANCE PLANNER (ORCHESTRATOR ENTRY)
    # ---------------------------------------------------------
    if agent_name in ("finance_planner", "finance"):
        plan_output = plan(prompt)

        if isinstance(plan_output, dict) and "steps" in plan_output:
            results: List[Dict[str, Any]] = []
            for step in plan_output["steps"]:
                agent = step.get("agent")
                input_data = step.get("input", "")
                step_result = _execute_finance_step(agent, input_data)
                results.append(
                    {
                        "agent": agent,
                        "input": input_data,
                        "output": step_result,
                    }
                )
            return results

        return "Finance planner returned an invalid plan format."

    # ---------------------------------------------------------
    # 2. DIRECT CALLS TO INDIVIDUAL BOTS
    # ---------------------------------------------------------
    if agent_name == "pos":
        bot = POSBot()
        return bot.run(prompt)

    if agent_name == "accounting":
        bot = AccountingBot()
        return bot.run(prompt)

    # ---------------------------------------------------------
    # 3. UNKNOWN AGENT
    # ---------------------------------------------------------
    return f"Unknown finance agent: {agent_name}"


def _execute_finance_step(agent: str, input_data: str) -> Any:
    """
    Internal helper to execute a single financial step.
    """

    if not agent:
        return "No agent specified in finance step."

    agent = agent.lower().strip()

    if agent == "pos":
        bot = POSBot()
        return bot.run(input_data)

    if agent == "accounting":
        bot = AccountingBot()
        return bot.run(input_data)

    return f"Unknown finance agent in plan: {agent}"
