from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler

app = Flask(__name__)

BOT_TOKEN = "7563988685:AAE0NDW9sksCzFzz4SlqX5aiJINseHhxxpY"
bot = Bot(token=BOT_TOKEN)
dispatcher = Dispatcher(bot, None, workers=0)

# دستور /start
def start(update, context):
    update.message.reply_text("سلام! ربات با وبهوک روشنه!")

# دستور /help
def help_command(update, context):
    update.message.reply_text("دستورهای ربات:\n/start\n/help")

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help_command))

@app.route('/')
def home():
    return "ربات آنلاین است! ✅"

@app.route(f'/webhook/{BOT_TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok'

if __name__ == '__main__':
    WEBHOOK_URL = f"https://my-telegram-bot-xc83.onrender.com/webhook/{BOT_TOKEN}"
    bot.set_webhook(WEBHOOK_URL)
    app.run(host='0.0.0.0', port=8080)
