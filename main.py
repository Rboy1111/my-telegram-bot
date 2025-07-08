from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler

import os

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dispatcher = Dispatcher(bot, None, workers=0)

def start(update, context):
    update.message.reply_text("سلام! ربات با وبهوک روشنه.")

dispatcher.add_handler(CommandHandler("start", start))

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK"

@app.route('/')
def index():
    return "ربات آنلاین است!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
