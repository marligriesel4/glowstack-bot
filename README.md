import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

BOT_TOKEN = "8811562415:AAHO5b_jHosAmlquS_TmOYUWeO5s2S1tGfY"
ADMIN_IDS = [7607613803]

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌿 Welcome to GlowStack Orders!\n\n"
        "Please send us your order using the format below:\n\n"
        "📦 Name:\n"
        "📦 Shipping Address:\n"
        "📦 Country:\n"
        "📦 Products & Quantities:\n"
        "📦 Payment Method:\n\n"
        "💳 PAYMENT OPTIONS:\n\n"
        "🇨🇦 Canada — Interac E-transfer\n"
        "🇺🇸 USA — Zelle or Cash App\n\n"
        "We will confirm your order and send payment details within 24 hours ✦"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text
    forward_msg = (
        f"📦 New Order Message\n\n"
        f"👤 From: {user.first_name} {user.last_name or ''}\n"
        f"🔗 Username: @{user.username or 'no username'}\n"
        f"🆔 User ID: {user.id}\n\n"
        f"💬 Message:\n{text}"
    )
    for admin_id in ADMIN_IDS:
        try:
            await context.bot.send_message(chat_id=admin_id, text=forward_msg)
        except Exception as e:
            logging.error(f"Could not send to admin {admin_id}: {e}")
    await update.message.reply_text(
        "✅ Thank you! Your order has been received.\n\n"
        "We will confirm your order and send payment details within 24 hours 🌿\n\n"
        "— GlowStack Team ✦"
    )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    caption = update.message.caption or "No caption"
    forward_msg = (
        f"📦 New Order — Photo\n\n"
        f"👤 From: {user.first_name} {user.last_name or ''}\n"
        f"🔗 Username: @{user.username or 'no username'}\n"
        f"🆔 User ID: {user.id}\n\n"
        f"📎 Caption: {caption}"
    )
    for admin_id in ADMIN_IDS:
        try:
            await context.bot.send_photo(chat_id=admin_id, photo=update.message.photo[-1].file_id, caption=forward_msg)
        except Exception as e:
            logging.error(f"Could not send photo to admin {admin_id}: {e}")
    await update.message.reply_text(
        "✅ Thank you! Your order has been received.\n\n"
        "We will confirm your order and send payment details within 24 hours 🌿\n\n"
        "— GlowStack Team ✦"
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
