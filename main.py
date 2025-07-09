from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, ConversationHandler, MessageHandler, filters
import smtplib
from email.mime.text import MIMEText

BOT_TOKEN = "7563988685:AAE0NDW9sksCzFzz4SlqX5aiJINseHhxxpY"

EMAIL_SENDER = "mahi1373ahmadi@gmail.com"
EMAIL_PASSWORD = "amolamol"  # توجه: بهتره از App Password واقعی استفاده کنی

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

GET_EMAIL = 1

def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("📷 دوربین", callback_data='camera')],
        [InlineKeyboardButton("🏢 معرفی شرکت", callback_data='company')],
        [InlineKeyboardButton("🛡️ خرید VPN", callback_data='vpn')],
        [InlineKeyboardButton("💬 نظرات مشتریان", callback_data='reviews')],
        [InlineKeyboardButton("📞 تماس با ما", callback_data='contact')],
        [InlineKeyboardButton("❓ راهنما", callback_data='help')]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "سلام!\n"
        "به ربات ما خوش آمدید. لطفا گزینه مورد نظر را انتخاب کنید:"
    )
    await update.message.reply_text(welcome_text, reply_markup=main_menu_keyboard())

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == 'camera':
        await query.edit_message_text("لطفا ایمیل خود را وارد کنید:")
        return GET_EMAIL

    # گزینه‌های دیگر
    await query.edit_message_text("دستور ناشناخته!", reply_markup=main_menu_keyboard())
    return ConversationHandler.END

async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    email = update.message.text

    subject = "پیام از ربات تلگرام"
    body = "You are so beautiful"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_SENDER
    msg['To'] = email

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, email, msg.as_string())
        server.quit()
        await update.message.reply_text(f"ایمیل به {email} ارسال شد. ممنون!")
    except Exception as e:
        await update.message.reply_text(f"خطا در ارسال ایمیل: {e}")

    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_handler, pattern='^camera$')],
        states={
            GET_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_email)]
        },
        fallbacks=[]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
