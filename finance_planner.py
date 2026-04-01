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

import shlex


def _extract_sale_tokens(query: str):
    """
    Try to parse patterns like:
      - "process sale coffee 5 USD"
      - "record sale sandwich 12.5 AUD"
    Returns (description, amount, currency) where possible.
    """
    q = query.strip()
    lower = q.lower()

    # Normalize leading phrase
    for prefix in ["process sale", "record sale", "make a sale"]:
        if lower.startswith(prefix):
            rest = q[len(prefix):].strip()
            break
    else:
        rest = q

    if not rest:
        return q, None, None

    parts = shlex.split(rest)
    if len(parts) >= 3:
        # Assume: item, amount, currency
        item = parts[0]
        amount_str = parts[1]
        currency = parts[2]
        try:
            amount = float(amount_str)
        except ValueError:
            amount = None

        description = f"{item} sale"
        return description, amount, currency

    # Fallback: treat whole thing as description
    return rest, None, None


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
        # Try to extract description, amount, currency
        desc, amount, currency = _extract_sale_tokens(query)

        # Build POS + Accounting commands with as much structure as we have
        pos_order_cmd = f"create_order description='{desc}'"
        if amount is not None:
            pos_order_cmd += f" amount='{amount}'"
        if currency:
            pos_order_cmd += f" currency='{currency}'"

        pos_payment_cmd = "create_payment_intent provider='stub' method='card'"
        if amount is not None:
            pos_payment_cmd += f" amount='{amount}'"
        if currency:
            pos_payment_cmd += f" currency='{currency}'"

        accounting_cmd = f"record_sale description='{desc}'"
        if amount is not None:
            accounting_cmd += f" amount='{amount}'"
        # default account stays "Sales" inside the bot

        return {
            "steps": [
                {
                    "agent": "pos",
                    "input": pos_order_cmd,
                },
                {
                    "agent": "pos",
                    "input": pos_payment_cmd,
                },
                {
                    "agent": "accounting",
                    "input": accounting_cmd,
                },
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
                    "input": query,
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
                    "input": query,
                }
            ]
        }

    # ---------------------------------------------------------
    # 4. DEFAULT: TRY POS FIRST, THEN ACCOUNTING ANALYSIS
    # ---------------------------------------------------------
    return {
        "steps": [
            {"agent": "pos", "input": query},
            {"agent": "accounting", "input": f"analyze_transaction description='{query}'"},
        ]
    }
