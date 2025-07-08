from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler

BOT_TOKEN = "7563988685:AAE0NDW9sksCzFzz4SlqX5aiJINseHhxxpY"

app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)
dispatcher = Dispatcher(bot, None, use_context=True)

# فرمان /start
def start(update, context):
    update.message.reply_text("سلام! ربات با webhook روشنه 🙂")

dispatcher.add_handler(CommandHandler("start", start))

@app.route('/')
def home():
    return "ربات آنلاین است! ✅"

# آدرس وبهوک تلگرام
@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
