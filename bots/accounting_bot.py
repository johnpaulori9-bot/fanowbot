# bots/accounting_bot.py
"""
Prototype accounting bot.

Handles:
- recording sales
- generating simple reports
- analyzing transactions

Data is stored in:
- JSON under data/finance/ledger.json (prototype)
- SQLite via memory_engine (for durable, queryable ledger)
"""

import os
import json
import uuid
import shlex
from datetime import datetime
from collections import defaultdict

from memory_engine import insert_ledger_entry, get_ledger_totals_by_account  # FIXED IMPORT


BASE_DIR = os.path.join(os.getcwd(), "data", "finance")
os.makedirs(BASE_DIR, exist_ok=True)

LEDGER_FILE = os.path.join(BASE_DIR, "ledger.json")


def _load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def _save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


class AccountingBot:
    """
    Prototype accounting bot.
    """

    def run(self, command: str):
        if not command:
            return "Empty accounting command."

        parts = shlex.split(command)
        action = parts[0]

        params = {}
        for item in parts[1:]:
            if "=" in item:
                key, value = item.split("=", 1)
                params[key] = value.strip("'").strip('"')

        if action == "record_sale":
            return self._record_sale(params)

        if action == "generate_report":
            return self._generate_report(params)

        if action == "analyze_transaction":
            return self._analyze_transaction(params)

        return f"Unknown accounting command: {action}"

    # ---------------------------------------------------------
    # RECORD SALE
    # ---------------------------------------------------------
    def _record_sale(self, params):
        ledger = _load_json(LEDGER_FILE)

        entry_id = str(uuid.uuid4())
        description = params.get("description", "No description provided.")
        amount = float(params.get("amount", "0") or 0)
        account = params.get("account", "Sales")
        created_at = datetime.utcnow().isoformat() + "Z"

        entry = {
            "entry_id": entry_id,
            "description": description,
            "amount": amount,
            "account": account,
            "created_at": created_at,
            "type": "sale",
        }

        ledger.append(entry)
        _save_json(LEDGER_FILE, ledger)

        insert_ledger_entry(
            description=description,
            amount=amount,
            account=account,
            entry_type="credit",
            entry_id=entry_id,
            customer_id=None,
        )

        return {
            "status": "sale_recorded",
            "entry": entry,
        }

    # ---------------------------------------------------------
    # GENERATE SIMPLE REPORT
    # ---------------------------------------------------------
    def _generate_report(self, params):
        report_type = params.get("type", "P&L").upper()
        period = params.get("period", "all")

        totals = get_ledger_totals_by_account(scope="global", customer_id=None)

        ledger = _load_json(LEDGER_FILE)

        return {
            "status": "ok",
            "report_type": report_type,
            "period": period,
            "totals_by_account": totals,
            "entries_count": len(ledger),
        }

    # ---------------------------------------------------------
    # ANALYZE TRANSACTION
    # ---------------------------------------------------------
    def _analyze_transaction(self, params):
        description = params.get("description", "")
        suggested_account = "Sales" if description else "Uncategorized"

        return {
            "status": "analyzed",
            "description": description,
            "suggested_account": suggested_account,
        }
