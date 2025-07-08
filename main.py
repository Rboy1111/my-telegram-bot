from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

app = Flask(__name__)

BOT_TOKEN = "7563988685:AAE0NDW9sksCzFzz4SlqX5aiJINseHhxxpY"

bot = Bot(token=BOT_TOKEN)
application = ApplicationBuilder().token(BOT_TOKEN).build()

@app.route('/')
def home():
    return "ربات آنلاین است! ✅"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! ربات با وبهوک روشنه!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("دستورهای ربات:\n/start\n/help")

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))

@app.route(f'/webhook/{BOT_TOKEN}', methods=['POST'])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot)
    await application.process_update(update)
    return 'ok'

if __name__ == '__main__':
    import asyncio
    WEBHOOK_URL = f"https://my-telegram-bot-xc83.onrender.com/webhook/{BOT_TOKEN}"
    asyncio.run(bot.set_webhook(WEBHOOK_URL))
    app.run(host='0.0.0.0', port=8080)
