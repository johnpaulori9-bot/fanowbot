# bots/pos_bot.py
"""
Prototype POS bot.

This bot does NOT process real payments yet.
It simulates:
- order creation
- payment intent creation
- receipt issuing

Data is stored in JSON files under data/finance/, so it is:
- simple
- portable
- easy to duplicate per customer later
"""

import os
import json
import uuid
import shlex
from datetime import datetime


BASE_DIR = os.path.join(os.getcwd(), "data", "finance")
os.makedirs(BASE_DIR, exist_ok=True)

ORDERS_FILE = os.path.join(BASE_DIR, "orders.json")
PAYMENTS_FILE = os.path.join(BASE_DIR, "payments.json")
RECEIPTS_FILE = os.path.join(BASE_DIR, "receipts.json")


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


class POSBot:
    """
    Prototype POS bot (no real payment processing).
    Handles orders, payment intents, and receipts.
    """

    def run(self, command: str):
        """
        Accepts commands like:
        - create_order description='Coffee sale to John' amount='5' currency='USD'
        - create_payment_intent provider='stub' method='card' amount='5' currency='USD'
        - issue_receipt order_id='...' channel='email'

        Or raw natural language, which it will wrap into a simple order.
        """

        if not command:
            return "Empty POS command."

        parts = shlex.split(command)
        action = parts[0]

        params = {}
        for item in parts[1:]:
            if "=" in item:
                key, value = item.split("=", 1)
                params[key] = value.strip("'").strip('"')

        if action == "create_order":
            return self._create_order(params)

        if action == "create_payment_intent":
            return self._create_payment_intent(params)

        if action == "issue_receipt":
            return self._issue_receipt(params)

        # Fallback: treat as simple order description
        return self._create_order({"description": command})

    # ---------------------------------------------------------
    # ORDER CREATION
    # ---------------------------------------------------------
    def _create_order(self, params):
        orders = _load_json(ORDERS_FILE)

        order_id = str(uuid.uuid4())
        description = params.get("description", "No description provided.")
        amount = float(params.get("amount", "0") or 0)
        currency = params.get("currency", "USD")
        created_at = datetime.utcnow().isoformat() + "Z"

        order = {
            "type": "order",
            "order_id": order_id,
            "description": description,
            "amount": amount,
            "currency": currency,
            "created_at": created_at,
            "status": "created"
        }

        orders.append(order)
        _save_json(ORDERS_FILE, orders)

        return {
            "status": "order_created",
            "order": order
        }

    # ---------------------------------------------------------
    # PAYMENT INTENT CREATION (STUB)
    # ---------------------------------------------------------
    def _create_payment_intent(self, params):
        payments = _load_json(PAYMENTS_FILE)

        payment_id = str(uuid.uuid4())
        provider = params.get("provider", "stub")
        method = params.get("method", "card")
        amount = float(params.get("amount", "0") or 0)
        currency = params.get("currency", "USD")
        created_at = datetime.utcnow().isoformat() + "Z"

        payment = {
            "type": "payment_intent",
            "payment_id": payment_id,
            "provider": provider,
            "method": method,
            "amount": amount,
            "currency": currency,
            "created_at": created_at,
            "status": "pending"
        }

        payments.append(payment)
        _save_json(PAYMENTS_FILE, payments)

        return {
            "status": "payment_intent_created",
            "payment": payment
        }

    # ---------------------------------------------------------
    # RECEIPT ISSUING
    # ---------------------------------------------------------
    def _issue_receipt(self, params):
        receipts = _load_json(RECEIPTS_FILE)

        receipt_id = str(uuid.uuid4())
        order_id = params.get("order_id", "unknown")
        channel = params.get("channel", "screen")
        created_at = datetime.utcnow().isoformat() + "Z"

        receipt = {
            "type": "receipt",
            "receipt_id": receipt_id,
            "order_id": order_id,
            "channel": channel,
            "created_at": created_at,
            "status": "issued"
        }

        receipts.append(receipt)
        _save_json(RECEIPTS_FILE, receipts)

        return {
            "status": "receipt_issued",
            "receipt": receipt
        }
