# telegram_bot.py
#
# FULL REPLACEMENT — POLLING VERSION (STABLE)
#
# This version works perfectly on Railway without needing a web server.
# Make sure your Telegram webhook is deleted before running this.

import telebot
import os
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
        "👋 Hybrid orchestrator online.\n\n"
        "Use:\n"
        "  /agent <agent_name> <prompt>\n"
        "  /finance <prompt>\n"
    )


# ---------------------------------------------------------
# UNIFIED /agent HANDLER
# ---------------------------------------------------------
@bot.message_handler(commands=['agent'])
def handle_agent(message):
    try:
        text = message.text.strip()
        parts = text.split(" ", 2)

        if len(parts) < 2:
            bot.reply_to(message, "Usage: /agent <agent_name> <prompt>")
            return

        agent_name = parts[1].strip()
        prompt = parts[2].strip() if len(parts) > 2 else ""
        agent_lower = agent_name.lower()

        if agent_lower in ("finance_planner", "finance", "pos", "accounting"):
            result = run_finance_agent(agent_lower, prompt)
        else:
            result = run_agent(agent_lower, prompt)

        bot.reply_to(message, str(result))

    except Exception as e:
        bot.reply_to(message, f"Error: {e}")


# ---------------------------------------------------------
# /finance SHORTCUT
# ---------------------------------------------------------
@bot.message_handler(commands=['finance'])
def handle_finance(message):
    try:
        text = message.text.strip()
        parts = text.split(" ", 1)

        if len(parts) < 2:
            bot.reply_to(message, "Usage: /finance <prompt>")
            return

        prompt = parts[1].strip()
        result = run_finance_agent("finance_planner", prompt)
        bot.reply_to(message, str(result))

    except Exception as e:
        bot.reply_to(message, f"Error: {e}")


# ---------------------------------------------------------
# FALLBACK
# ---------------------------------------------------------
@bot.message_handler(func=lambda m: True)
def handle_fallback(message):
    bot.reply_to(message,
        "Unknown command.\n"
        "Try:\n"
        "  /agent planner <prompt>\n"
        "  /finance <prompt>\n"
    )


# ---------------------------------------------------------
# POLLING LOOP
# ---------------------------------------------------------
print("Telegram bot is running...")
bot.infinity_polling()
