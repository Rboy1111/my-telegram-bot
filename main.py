from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

from flask import Flask
from threading import Thread

BOT_TOKEN = "7563988685:AAE0NDW9sksCzFzz4SlqX5aiJINseHhxxpY"

# Flask server to keep the app alive on Render
app = Flask('')

@app.route('/')
def home():
    return "Bot is running."

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🏢 معرفی شرکت", callback_data='company')],
        [InlineKeyboardButton("🛡️ خرید VPN", callback_data='vpn')],
        [InlineKeyboardButton("💬 نظرات مشتریان", callback_data='reviews')],
        [InlineKeyboardButton("📞 تماس با ما", callback_data='contact')],
        [InlineKeyboardButton("❓ راهنما", callback_data='help')]
    ]
    return InlineKeyboardMarkup(keyboard)

def vpn_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🌐 خرید اشتراک ماهانه", callback_data='buy_monthly')],
        [InlineKeyboardButton("🌐 خرید اشتراک سالانه", callback_data='buy_yearly')],
        [InlineKeyboardButton("⬅️ بازگشت به منوی اصلی", callback_data='main_menu')]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "سلام!\n"
        "به ربات رسمی شرکت ما خوش آمدید. با این ربات می‌توانید:\n"
        "✅ با شرکت ما آشنا شوید\n"
        "✅ خدمات VPN ما را خریداری کنید\n"
        "✅ نظرات مشتریان را بخوانید\n"
        "✅ با ما تماس بگیرید\n"
        "\nلطفا یکی از گزینه‌ها را انتخاب کنید:"
    )
    await update.message.reply_text(welcome_text, reply_markup=main_menu_keyboard())

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "/start - شروع\n"
        "/help - راهنمای استفاده\n"
        "از منوی دکمه‌ها استفاده کنید."
    )
    await update.message.reply_text(help_text)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == 'main_menu':
        await query.edit_message_text(
            "به منوی اصلی بازگشتید. لطفا گزینه مورد نظر را انتخاب کنید:",
            reply_markup=main_menu_keyboard()
        )
    elif data == 'company':
        company_text = (
            "🏢 شرکت ما:\n"
            "شرکت [نام شرکت شما] با بیش از ۱۰ سال سابقه در زمینه خدمات فناوری اطلاعات و امنیت شبکه فعالیت می‌کند.\n"
            "ما متعهد به ارائه بهترین خدمات VPN با بالاترین کیفیت و پشتیبانی ۲۴/۷ هستیم.\n"
            "برای کسب اطلاعات بیشتر به وبسایت ما مراجعه کنید:\n"
            "https://example.com"
        )
        await query.edit_message_text(company_text, reply_markup=main_menu_keyboard())
    elif data == 'vpn':
        await query.edit_message_text(
            "🛡️ خدمات VPN ما:\n"
            "شما می‌توانید اشتراک‌های متنوع ماهانه و سالانه را خریداری کنید.\n"
            "لطفا نوع اشتراک مورد نظر خود را انتخاب کنید:",
            reply_markup=vpn_menu_keyboard()
        )
    elif data == 'buy_monthly':
        await query.edit_message_text(
            "🌐 اشتراک ماهانه VPN فقط با ۹۹ هزار تومان.\n"
            "برای خرید و پرداخت به این لینک مراجعه کنید:\n"
            "https://example.com/buy_monthly"
        )
    elif data == 'buy_yearly':
        await query.edit_message_text(
            "🌐 اشتراک سالانه VPN فقط با ۹۹۹ هزار تومان.\n"
            "برای خرید و پرداخت به این لینک مراجعه کنید:\n"
            "https://example.com/buy_yearly"
        )
    elif data == 'reviews':
        reviews_text = (
            "💬 نظرات مشتریان ما:\n"
            "⭐️⭐️⭐️⭐️⭐️  \n"
            "این سرویس عالیه، پشتیبانی فوق العاده و سرعت عالی.\n\n"
            "⭐️⭐️⭐️⭐️⭐️  \n"
            "من همیشه از این VPN استفاده می‌کنم و راضی‌ام."
        )
        await query.edit_message_text(reviews_text, reply_markup=main_menu_keyboard())
    elif data == 'contact':
        contact_text = (
            "📞 تماس با ما:\n"
            "تلفن: ۰۱۲۳۴۵۶۷۸۹\n"
            "ایمیل: info@example.com\n"
            "اینستاگرام: https://instagram.com/yourcompany\n"
            "تلگرام: @yourcompany"
        )
        await query.edit_message_text(contact_text, reply_markup=main_menu_keyboard())
    elif data == 'help':
        await query.edit_message_text(
            "برای استفاده از ربات از منوی دکمه‌ها استفاده کنید.\n"
            "در صورت نیاز به راهنمایی بیشتر با پشتیبانی تماس بگیرید.",
            reply_markup=main_menu_keyboard()
        )
    else:
        await query.edit_message_text("دستور ناشناخته! لطفا دوباره تلاش کنید.", reply_markup=main_menu_keyboard())

def main():
    keep_alive()  # روشن نگه داشتن اپلیکیشن در Render با سرور Flask
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
