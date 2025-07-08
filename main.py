from fastapi import FastAPI, Request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, Dispatcher
import uvicorn
import os

BOT_TOKEN = "7563988685:AAE0NDW9sksCzFzz4SlqX5aiJINseHhxxpY"
app = FastAPI()
bot = Bot(token=BOT_TOKEN)
application = ApplicationBuilder().token(BOT_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! ربات همیشه روشنه 😎")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("دستورهای ربات:\n/start\n/help")

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))

@app.post("/webhook")
async def telegram_webhook(req: Request):
    data = await req.json()
    update = Update.de_json(data, bot)
    await application.process_update(update)
    return {"ok": True}

@app.get("/")
def read_root():
    return {"message": "ربات آنلاین است! ✅"}

if __name__ == "__main__":
    # آدرس و پورت را برای uvicorn می‌گیریم یا مقدار پیش‌فرض می‌دهیم
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
