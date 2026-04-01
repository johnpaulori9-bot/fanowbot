# telegram_bot.py
#
# FULL REPLACEMENT FILE
# Unified Telegram handler for:
# - Main orchestrator (planner → advisor → originator)
# - Financial orchestrator (finance_planner → pos → accounting)
#
# Supports:
#   /agent <agent_name> <prompt>
#   /finance <prompt>
#
# This file is clean, stable, and ready for expansion.

import telebot
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is missing from environment variables.")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# ---------------------------------------------------------
# IMPORT ORCHESTRATORS
# ---------------------------------------------------------
from agent_router import run_agent
from finance_router import run_finance_agent


# ---------------------------------------------------------
# START COMMAND
# ---------------------------------------------------------
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message,
        "👋 Hello! Your hybrid orchestrator is online.\n\n"
        "Use:\n"
        "  /agent <agent_name> <prompt>\n"
        "  /finance <prompt>\n\n"
        "Examples:\n"
        "  /agent planner create a workflow for land management\n"
        "  /agent finance_planner process sale coffee 5 USD\n"
        "  /finance process sale coffee 5 USD\n"
    )


# ---------------------------------------------------------
# UNIFIED /agent HANDLER
# ---------------------------------------------------------
@bot.message_handler(commands=['agent'])
def handle_agent(message):
    """
    Unified /agent command handler.
    Routes financial agents to finance_router,
    and all other agents to the main agent_router.
    """

    try:
        text = message.text.strip()

        # Split into: /agent <agent_name> <prompt>
        parts = text.split(" ", 2)

        if len(parts) < 2:
            bot.reply_to(message, "Usage: /agent <agent_name> <prompt>")
            return

        agent_name = parts[1].strip()
        prompt = parts[2].strip() if len(parts) > 2 else ""

        agent_lower = agent_name.lower()

        # ---------------------------------------------------------
        # FINANCIAL AGENTS
        # ---------------------------------------------------------
        if agent_lower in ("finance_planner", "finance", "pos", "accounting"):
            result = run_finance_agent(agent_lower, prompt)
            bot.reply_to(message, str(result))
            return

        # ---------------------------------------------------------
        # MAIN ORCHESTRATOR AGENTS
        # ---------------------------------------------------------
        result = run_agent(agent_lower, prompt)
        bot.reply_to(message, str(result))

    except Exception as e:
        bot.reply_to(message, f"Error: {e}")


# ---------------------------------------------------------
# /finance SHORTCUT COMMAND
# ---------------------------------------------------------
@bot.message_handler(commands=['finance'])
def handle_finance(message):
    """
    Shortcut command for financial planner.
    Equivalent to: /agent finance_planner <prompt>
    """

    try:
        text = message.text.strip()
        parts = text.split(" ", 1)

        if len(parts) < 2:
            bot.reply_to(message, "Usage: /finance <prompt>")
            return

        prompt = parts[1].strip()

        # Always go through the financial planner
        result = run_finance_agent("finance_planner", prompt)
        bot.reply_to(message, str(result))

    except Exception as e:
        bot.reply_to(message, f"Error: {e}")


# ---------------------------------------------------------
# FALLBACK: ECHO ANY OTHER MESSAGE
# ---------------------------------------------------------
@bot.message_handler(func=lambda m: True)
def handle_fallback(message):
    bot.reply_to(message,
        "I didn’t recognize that command.\n\n"
        "Try:\n"
        "  /agent planner <prompt>\n"
        "  /agent finance_planner <prompt>\n"
        "  /finance <prompt>\n"
    )


# ---------------------------------------------------------
# BOT POLLING
# ---------------------------------------------------------
print("Telegram bot is running...")
bot.infinity_polling()
