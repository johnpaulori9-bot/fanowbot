import telebot
import datetime

# ---------------------------------------------------------
# INSERT YOUR BOT TOKEN HERE
# ---------------------------------------------------------
BOT_TOKEN = "8650673001:AAFbfsP4sPFO40XHZ8IVCsqPmBAws_2qMn4"

bot = telebot.TeleBot(BOT_TOKEN)

# ---------------------------------------------------------
# /start command
# ---------------------------------------------------------
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,
                 "FanowBot is online.\n"
                 "Use /help to see available commands.")

# ---------------------------------------------------------
# /help command
# ---------------------------------------------------------
@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message,
                 "Available commands:\n"
                 "/start - Initialize the bot\n"
                 "/help - Show this help menu\n"
                 "/status - Check if the bot is running\n"
                 "/echo <text> - Repeat your message\n"
                 "/about - About this bot\n"
                 "/version - Bot version\n"
                 "/time - Server time\n"
                 "/ping - Check responsiveness")

# ---------------------------------------------------------
# /status command
# ---------------------------------------------------------
@bot.message_handler(commands=['status'])
def status(message):
    bot.reply_to(message, "Status: Online and ready.")

# ---------------------------------------------------------
# /echo command
# ---------------------------------------------------------
@bot.message_handler(commands=['echo'])
def echo(message):
    text = message.text.replace("/echo", "").strip()
    if text:
        bot.reply_to(message, text)
    else:
        bot.reply_to(message, "Usage: /echo <text>")

# ---------------------------------------------------------
# /about command
# ---------------------------------------------------------
@bot.message_handler(commands=['about'])
def about(message):
    bot.reply_to(message,
                 "FanowBot — your mobile-first command interface.\n"
                 "Built for Chuuk workflows, OS automation, and knowledge ingestion.")

# ---------------------------------------------------------
# /version command
# ---------------------------------------------------------
@bot.message_handler(commands=['version'])
def version(message):
    bot.reply_to(message, "FanowBot version 0.2 — Command Framework Online.")

# ---------------------------------------------------------
# /time command
# ---------------------------------------------------------
@bot.message_handler(commands=['time'])
def time_cmd(message):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    bot.reply_to(message, f"Server time: {now}")

# ---------------------------------------------------------
# /ping command
# ---------------------------------------------------------
@bot.message_handler(commands=['ping'])
def ping(message):
    bot.reply_to(message, "pong")

# ---------------------------------------------------------
# Fallback handler (anything else)
# ---------------------------------------------------------
@bot.message_handler(func=lambda message: True)
def fallback(message):
    bot.reply_to(message, f"You said: {message.text}")

# ---------------------------------------------------------
# START BOT
# ---------------------------------------------------------
print("Telegram bot is running...")
bot.infinity_polling()

