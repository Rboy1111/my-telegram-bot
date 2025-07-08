import logging
from telegram import Update, ForceReply
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = "7563988685:AAE0NDW9sksCzFzz4SlqX5aiJINseHhxxpY"

# تنظیمات لاگ
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# حافظه ساده برای ذخیره داده‌ها (موقتی)
user_data_store = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_html(
        rf"سلام <b>{user.first_name}</b>! به ربات حرفه‌ای من خوش آمدی.\n"
        "برای راهنما /help را بزنید."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "دستورهای موجود:\n"
        "/start - شروع کار با ربات\n"
        "/help - نمایش راهنما\n"
        "/echo - تکرار پیامی که ارسال می‌کنید\n"
        "/info - دریافت اطلاعات درباره شما\n"
        "/save <متن> - ذخیره یک متن برای شما\n"
        "/show - نمایش متنی که ذخیره کردید\n"
    )
    await update.message.reply_text(help_text)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # تکرار همان پیامی که کاربر فرستاده
    await update.message.reply_text(update.message.text)

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    info_text = (
        f"شناسه شما: {user.id}\n"
        f"نام شما: {user.first_name}\n"
        f"نام کاربری: @{user.username if user.username else 'ندارد'}"
    )
    await update.message.reply_text(info_text)

async def save_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text_to_save = " ".join(context.args)
    if not text_to_save:
        await update.message.reply_text("لطفا متنی برای ذخیره ارسال کنید. مثال:\n/save سلام")
        return
    user_data_store[user_id] = text_to_save
    await update.message.reply_text("متن شما ذخیره شد!")

async def show_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    saved_text = user_data_store.get(user_id)
    if saved_text:
        await update.message.reply_text(f"متن ذخیره شده شما:\n{saved_text}")
    else:
        await update.message.reply_text("هیچ متنی ذخیره نشده است.")

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "دستور ناشناخته است. لطفا /help را برای مشاهده دستورات استفاده کنید."
    )

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(msg="Exception while handling an update:", exc_info=context.error)
    if update and hasattr(update, "message") and update.message:
        await update.message.reply_text(
            "خطایی رخ داد. لطفا دوباره تلاش کنید."
        )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("echo", echo))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("save", save_text))
    app.add_handler(CommandHandler("show", show_text))

    # مدیریت پیام‌های ناشناخته
    app.add_handler(MessageHandler(filters.COMMAND, unknown))

    # مدیریت خطا
    app.add_error_handler(error_handler)

    logger.info("ربات حرفه‌ای شروع به کار کرد.")
    app.run_polling()

if __name__ == "__main__":
    main()
