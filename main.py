from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

app = Flask(__name__)

BOT_TOKEN = "7563988685:AAE0NDW9sksCzFzz4SlqX5aiJINseHhxxpY"

@app.route('/')
def home():
    return "ربات آنلاین است! ✅"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! ربات همیشه روشنه 😎")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("دستورهای ربات:\n/start\n/help")

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def main():
    # اجرای Flask در یک Thread جداگانه
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # ساخت و اجرای ربات تلگرام
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.run_polling()

if __name__ == '__main__':
    main()
