import telebot
import os
import json
from datetime import datetime

# ============================================================
#  LOAD BOT TOKEN
# ============================================================
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# ============================================================
#  PERSONALITY ENGINE
# ============================================================
def respond(mode, text):
    """
    Hybrid personality engine.
    Mode determines tone:
    - assistant: friendly
    - professional: structured
    - agent: authoritative
    - admin: private, powerful
    """
    if mode == "assistant":
        return f"🤝 Sure thing! {text}"
    elif mode == "professional":
        return f"📄 Understood. {text}"
    elif mode == "agent":
        return f"⚙️ Executing. {text}"
    elif mode == "admin":
        return f"🔐 Admin mode active. {text}"
    else:
        return text

# ============================================================
#  MEMORY SYSTEM (simple JSON, expandable later)
# ============================================================
MEMORY_FILE = "memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ============================================================
#  START COMMAND
# ============================================================
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        respond("assistant",
        "I'm online and ready. I can assist you, run agents, plan tasks, or automate workflows.")
    )

# ============================================================
#  HELP COMMAND
# ============================================================
@bot.message_handler(commands=['help'])
def help_cmd(message):
    help_text = """
Available Commands:
/start - Initialize the bot
/help - Show this help menu
/status - System status
/task - Create or manage tasks
/plan - Planning assistant
/agent - Agent control mode
/workflow - Workflow execution
/admin - Admin-only commands
"""
    bot.reply_to(message, respond("assistant", help_text))

# ============================================================
#  STATUS COMMAND
# ============================================================
@bot.message_handler(commands=['status'])
def status(message):
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    bot.reply_to(
        message,
        respond("professional", f"System online. Timestamp: {now}")
    )

# ============================================================
#  TASK COMMAND
# ============================================================
@bot.message_handler(commands=['task'])
def task(message):
    bot.reply_to(
        message,
        respond("assistant", "What task would you like to create or manage?")
    )

# ============================================================
#  PLAN COMMAND
# ============================================================
@bot.message_handler(commands=['plan'])
def plan(message):
    bot.reply_to(
        message,
        respond("assistant", "Tell me what you want to plan, and I’ll break it down.")
    )

# ============================================================
#  AGENT COMMAND
# ============================================================
@bot.message_handler(commands=['agent'])
def agent_handler(message):
    """
    Unified /agent entrypoint.

    Usage examples (natural language):
    - /agent planner create a workflow for land management
    - /agent advisor help me plan my week
    - /agent originator restore_forest area=50 priority=high
    """

    try:
        # Remove the command itself and trim whitespace
        text = message.text.replace("/agent", "", 1).strip()

        # If user only typed /agent with nothing else
        if not text:
            bot.reply_to(
                message,
                "Agent mode activated.\n\n"
                "Tell me what you want the agent system to do.\n\n"
                "Examples:\n"
                "- /agent planner create a workflow for GIS governance\n"
                "- /agent advisor help me prioritize my tasks\n"
                "- /agent originator restore_forest area=50 priority=high"
            )
            return

        # Split into: first word = agent name, rest = prompt
        parts = text.split()
        agent_name = parts[0].lower()
        prompt = " ".join(parts[1:]) if len(parts) > 1 else ""

        # Import the router here to avoid circular imports at module load time
        from agent_router import run_agent

        # Call the unified agent router
        result = run_agent(agent_name, prompt)

        # Reply with the result
        bot.reply_to(
            message,
            f"🔧 Agent `{agent_name}` executed.\n\nResult:\n{result}"
        )

    except Exception as e:
        # Catch any error and show it in a controlled way
        bot.reply_to(
            message,
            f"⚠️ Error while running agent `{agent_name}`:\n{e}"
        )


# ============================================================
#  WORKFLOW COMMAND
# ============================================================
@bot.message_handler(commands=['workflow'])
def workflow(message):
    bot.reply_to(
        message,
        respond("agent", "Workflow mode active. Describe the workflow you want executed.")
    )

# ============================================================
#  ADMIN COMMAND (restricted)
# ============================================================
ADMIN_USER_ID = None  # You can set your Telegram ID here

@bot.message_handler(commands=['admin'])
def admin(message):
    if ADMIN_USER_ID and message.from_user.id != ADMIN_USER_ID:
        bot.reply_to(message, "Unauthorized.")
        return

    bot.reply_to(
        message,
        respond("admin", "Admin mode ready. What system command do you want to run?")
    )

# ============================================================
#  FALLBACK HANDLER
# ============================================================
@bot.message_handler(func=lambda m: True)
def fallback(message):
    bot.reply_to(
        message,
        respond("assistant", "I’m here. Tell me what you need.")
    )

# ============================================================
#  RUN BOT
# ============================================================
print("Telegram bot is running...")
bot.infinity_polling()
