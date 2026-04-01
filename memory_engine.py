# memory_engine.py
#
# Hybrid memory engine:
# - Global DB:   /app/data/finance/finance.db
# - Per-customer DB: /app/data/customers/<customer_id>/finance.db
#
# POS + Accounting will write to both JSON (for prototype) and SQLite (for durability).
# Finance planner and routers will query via this engine.

import os
import sqlite3
from typing import Any, Dict, List, Optional, Tuple

BASE_DATA_DIR = os.getenv("DATA_DIR", "/app/data")
GLOBAL_DB_PATH = os.path.join(BASE_DATA_DIR, "finance", "finance.db")


# ---------------------------------------------------------
# PATH HELPERS
# ---------------------------------------------------------
def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def get_global_db_path() -> str:
    dir_path = os.path.dirname(GLOBAL_DB_PATH)
    ensure_dir(dir_path)
    return GLOBAL_DB_PATH


def get_customer_db_path(customer_id: str) -> str:
    safe_id = customer_id.replace("/", "_")
    dir_path = os.path.join(BASE_DATA_DIR, "customers", safe_id)
    ensure_dir(dir_path)
    return os.path.join(dir_path, "finance.db")


# ---------------------------------------------------------
# CONNECTION + SCHEMA
# ---------------------------------------------------------
def get_connection(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    initialize_schema(conn)
    return conn


def initialize_schema(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()

    # Orders
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id TEXT UNIQUE,
            description TEXT,
            amount REAL,
            currency TEXT,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Payments
    cur.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            payment_id TEXT UNIQUE,
            order_id TEXT,
            provider TEXT,
            method TEXT,
            amount REAL,
            currency TEXT,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Receipts
    cur.execute("""
        CREATE TABLE IF NOT EXISTS receipts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            receipt_id TEXT UNIQUE,
            order_id TEXT,
            payment_id TEXT,
            description TEXT,
            amount REAL,
            currency TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Ledger
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ledger (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_id TEXT UNIQUE,
            description TEXT,
            amount REAL,
            account TEXT,
            entry_type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Customers (for future multi-tenant metadata)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id TEXT UNIQUE,
            name TEXT,
            metadata TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Sessions (for conversational context)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT UNIQUE,
            customer_id TEXT,
            metadata TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Memory (for long-term notes / embeddings later)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id TEXT,
            session_id TEXT,
            role TEXT,
            content TEXT,
            tags TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()


# ---------------------------------------------------------
# INSERT HELPERS (GLOBAL OR CUSTOMER)
# ---------------------------------------------------------
def _get_db_path(scope: str, customer_id: Optional[str] = None) -> str:
    if scope == "global":
        return get_global_db_path()
    elif scope == "customer":
        if not customer_id:
            raise ValueError("customer_id is required for customer scope")
        return get_customer_db_path(customer_id)
    else:
        raise ValueError(f"Unknown scope: {scope}")


def insert_order(scope: str, order: Dict[str, Any], customer_id: Optional[str] = None) -> None:
    db_path = _get_db_path(scope, customer_id)
    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute("""
        INSERT OR IGNORE INTO orders (order_id, description, amount, currency, status)
        VALUES (?, ?, ?, ?, ?)
    """, (
        order.get("order_id"),
        order.get("description"),
        float(order.get("amount", 0)),
        order.get("currency"),
        order.get("status", "created"),
    ))
    conn.commit()
    conn.close()


def insert_payment(scope: str, payment: Dict[str, Any], customer_id: Optional[str] = None) -> None:
    db_path = _get_db_path(scope, customer_id)
    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute("""
        INSERT OR IGNORE INTO payments (payment_id, order_id, provider, method, amount, currency, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        payment.get("payment_id"),
        payment.get("order_id"),
        payment.get("provider"),
        payment.get("method"),
        float(payment.get("amount", 0)),
        payment.get("currency"),
        payment.get("status", "created"),
    ))
    conn.commit()
    conn.close()


def insert_receipt(scope: str, receipt: Dict[str, Any], customer_id: Optional[str] = None) -> None:
    db_path = _get_db_path(scope, customer_id)
    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute("""
        INSERT OR IGNORE INTO receipts (receipt_id, order_id, payment_id, description, amount, currency)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        receipt.get("receipt_id"),
        receipt.get("order_id"),
        receipt.get("payment_id"),
        receipt.get("description"),
        float(receipt.get("amount", 0)),
        receipt.get("currency"),
    ))
    conn.commit()
    conn.close()


def insert_ledger_entry(scope: str, entry: Dict[str, Any], customer_id: Optional[str] = None) -> None:
    db_path = _get_db_path(scope, customer_id)
    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute("""
        INSERT OR IGNORE INTO ledger (entry_id, description, amount, account, entry_type)
        VALUES (?, ?, ?, ?, ?)
    """, (
        entry.get("entry_id"),
        entry.get("description"),
        float(entry.get("amount", 0)),
        entry.get("account"),
        entry.get("entry_type", "credit"),
    ))
    conn.commit()
    conn.close()


# ---------------------------------------------------------
# QUERY HELPERS (REPORTING)
# ---------------------------------------------------------
def get_ledger_totals_by_account(scope: str, customer_id: Optional[str] = None) -> Dict[str, float]:
    db_path = _get_db_path(scope, customer_id)
    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute("""
        SELECT account, SUM(amount) as total
        FROM ledger
        GROUP BY account
    """)
    rows = cur.fetchall()
    conn.close()
    return {row["account"]: float(row["total"]) for row in rows}


def get_orders(scope: str, customer_id: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
    db_path = _get_db_path(scope, customer_id)
    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute("""
        SELECT order_id, description, amount, currency, status, created_at
        FROM orders
        ORDER BY created_at DESC
        LIMIT ?
    """, (limit,))
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]


# ---------------------------------------------------------
# MEMORY / SESSIONS (for future use)
# ---------------------------------------------------------
def add_memory(scope: str, content: str, customer_id: Optional[str] = None,
               session_id: Optional[str] = None, role: str = "system",
               tags: Optional[str] = None) -> None:
    db_path = _get_db_path(scope, customer_id)
    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO memory (customer_id, session_id, role, content, tags)
        VALUES (?, ?, ?, ?, ?)
    """, (customer_id, session_id, role, content, tags))
    conn.commit()
    conn.close()


def get_memory(scope: str, customer_id: Optional[str] = None,
               session_id: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
    db_path = _get_db_path(scope, customer_id)
    conn = get_connection(db_path)
    cur = conn.cursor()

    if session_id:
        cur.execute("""
            SELECT customer_id, session_id, role, content, tags, created_at
            FROM memory
            WHERE customer_id = ? AND session_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        """, (customer_id, session_id, limit))
    else:
        cur.execute("""
            SELECT customer_id, session_id, role, content, tags, created_at
            FROM memory
            WHERE customer_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        """, (customer_id, limit))

    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]
