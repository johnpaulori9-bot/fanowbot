# memory_engine.py
"""
Unified SQLite memory engine for:
- POS orders
- POS payments
- Accounting ledger entries

Supports:
- Global scope (customer_id=None)
- Future per-customer DBs
"""

import os
import sqlite3
from typing import Optional, Dict, Any, List


# ---------------------------------------------------------
# DATABASE LOCATION
# ---------------------------------------------------------
BASE_DIR = os.getenv("DATA_DIR", "/app/data")
DB_PATH = os.path.join(BASE_DIR, "finance.db")

os.makedirs(BASE_DIR, exist_ok=True)


# ---------------------------------------------------------
# CONNECTION HELPER
# ---------------------------------------------------------
def _get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ---------------------------------------------------------
# TABLE CREATION
# ---------------------------------------------------------
def _init_db():
    conn = _get_conn()
    cur = conn.cursor()

    # Orders
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            description TEXT,
            amount REAL,
            currency TEXT,
            status TEXT,
            customer_id TEXT,
            created_at TEXT
        )
    """)

    # Payments
    cur.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            payment_id TEXT PRIMARY KEY,
            order_id TEXT,
            provider TEXT,
            method TEXT,
            amount REAL,
            currency TEXT,
            status TEXT,
            customer_id TEXT,
            created_at TEXT
        )
    """)

    # Ledger
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ledger (
            entry_id TEXT PRIMARY KEY,
            description TEXT,
            amount REAL,
            account TEXT,
            entry_type TEXT,
            customer_id TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


_init_db()


# ---------------------------------------------------------
# INSERT ORDER
# ---------------------------------------------------------
def insert_order(
    order_id: str,
    description: str,
    amount: float,
    currency: str,
    status: str,
    customer_id: Optional[str] = None,
    created_at: Optional[str] = None,
) -> Dict[str, Any]:

    conn = _get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO orders (order_id, description, amount, currency, status, customer_id, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (order_id, description, amount, currency, status, customer_id, created_at))

    conn.commit()
    conn.close()

    return {
        "order_id": order_id,
        "description": description,
        "amount": amount,
        "currency": currency,
        "status": status,
        "customer_id": customer_id,
        "created_at": created_at,
    }


# ---------------------------------------------------------
# INSERT PAYMENT
# ---------------------------------------------------------
def insert_payment(
    payment_id: str,
    order_id: str,
    provider: str,
    method: str,
    amount: float,
    currency: str,
    status: str,
    customer_id: Optional[str] = None,
    created_at: Optional[str] = None,
) -> Dict[str, Any]:

    conn = _get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO payments (payment_id, order_id, provider, method, amount, currency, status, customer_id, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (payment_id, order_id, provider, method, amount, currency, status, customer_id, created_at))

    conn.commit()
    conn.close()

    return {
        "payment_id": payment_id,
        "order_id": order_id,
        "provider": provider,
        "method": method,
        "amount": amount,
        "currency": currency,
        "status": status,
        "customer_id": customer_id,
        "created_at": created_at,
    }


# ---------------------------------------------------------
# INSERT LEDGER ENTRY
# ---------------------------------------------------------
def insert_ledger_entry(
    entry_id: str,
    description: str,
    amount: float,
    account: str,
    entry_type: str,
    customer_id: Optional[str] = None,
    created_at: Optional[str] = None,
) -> Dict[str, Any]:

    conn = _get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO ledger (entry_id, description, amount, account, entry_type, customer_id, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (entry_id, description, amount, account, entry_type, customer_id, created_at))

    conn.commit()
    conn.close()

    return {
        "entry_id": entry_id,
        "description": description,
        "amount": amount,
        "account": account,
        "entry_type": entry_type,
        "customer_id": customer_id,
        "created_at": created_at,
    }


# ---------------------------------------------------------
# LEDGER TOTALS
# ---------------------------------------------------------
def get_ledger_totals_by_account(scope="global", customer_id=None) -> Dict[str, float]:
    conn = _get_conn()
    cur = conn.cursor()

    if customer_id:
        cur.execute("""
            SELECT account, SUM(amount) AS total
            FROM ledger
            WHERE customer_id = ?
            GROUP BY account
        """, (customer_id,))
    else:
        cur.execute("""
            SELECT account, SUM(amount) AS total
            FROM ledger
            GROUP BY account
        """)

    rows = cur.fetchall()
    conn.close()

    return {row["account"]: row["total"] for row in rows}
