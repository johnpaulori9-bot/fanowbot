# finance_planner.py
"""
Financial planner for orchestrator mode.

Given a natural language query about money, sales, or accounting,
returns a multi-step plan:

    {
      "steps": [
        { "agent": "pos", "input": "..." },
        { "agent": "accounting", "input": "..." }
      ]
    }

This is the financial equivalent of your main planner, but scoped to
payments, sales, and accounting flows.
"""


def plan(query: str):
    """
    Main entry point for the financial planner.

    :param query: Natural language user request.
    :return: Dict with a "steps" list describing which financial agents to call.
    """
    q = query.lower().strip()

    # ---------------------------------------------------------
    # 1. HIGH-LEVEL "PROCESS SALE" REQUESTS
    # ---------------------------------------------------------
    if "process sale" in q or "record sale" in q or "make a sale" in q:
        # For now, we treat the entire query as the sale description.
        sale_desc = query.strip()

        return {
            "steps": [
                {
                    "agent": "pos",
                    "input": f"create_order description='{sale_desc}'"
                },
                {
                    "agent": "pos",
                    "input": "create_payment_intent provider='stub' method='card'"
                },
                {
                    "agent": "accounting",
                    "input": f"record_sale description='{sale_desc}'"
                }
            ]
        }

    # ---------------------------------------------------------
    # 2. POS-FOCUSED REQUESTS
    # ---------------------------------------------------------
    if any(k in q for k in ["pos", "point of sale", "payment", "card", "checkout", "order"]):
        return {
            "steps": [
                {
                    "agent": "pos",
                    "input": query
                }
            ]
        }

    # ---------------------------------------------------------
    # 3. ACCOUNTING-FOCUSED REQUESTS
    # ---------------------------------------------------------
    if any(k in q for k in ["accounting", "ledger", "report", "p&l", "profit and loss", "balance sheet"]):
        return {
            "steps": [
                {
                    "agent": "accounting",
                    "input": query
                }
            ]
        }

    # ---------------------------------------------------------
    # 4. DEFAULT: TRY POS FIRST, THEN ACCOUNTING ANALYSIS
    # ---------------------------------------------------------
    return {
        "steps": [
            {"agent": "pos", "input": query},
            {"agent": "accounting", "input": f"analyze_transaction description='{query}'"}
        ]
    }
