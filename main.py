from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

app = Flask(__name__)

# توکن ربات شما (در آینده حتماً با روش امن‌تر جایگزینش کن!)
BOT_TOKEN = "7563988685:AAE0NDW9sksCzFzz4SlqX5aiJINseHhxxpY"

@app.route('/')
def home():
    return "ربات آنلاین است! ✅"

# دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! ربات همیشه روشنه 😎")

# دستور /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("دستورهای ربات:\n/start\n/help")

def run():
    app.run(host='0.0.0.0', port=8080)

def start_flask():
    thread = Thread(target=run)
    thread.start()

def main():
    start_flask()
    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("help", help_command))
    app_bot.run_polling()

if __name__ == '__main__':
    main()
