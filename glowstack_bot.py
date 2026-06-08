import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

# ── CONFIG ──────────────────────────────────────────────
BOT_TOKEN = "8811562415:AAHO5b_jHosAmlquS_TmOYUWeO5s2S1tGfY"
ADMIN_IDS = [7607613803]  # Add co-admin ID here later e.g. [7607613803, 123456789]
# ────────────────────────────────────────────────────────

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌿 Welcome to GlowStack Orders!\n\n"
        "Please send us your order in this format:\n\n"
        "📦 *Name:*\n"
        "📦 *Shipping Address:*\n"
        "📦 *Country:*\n"
        "📦 *Products & Quantities:*\n"
        "📦 *Payment Method:* E-transfer / Cash App / Crypto\n\n"
        "We will get back to you within 24 hours ✦",
        parse_mode="Markdown"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text

    # Build the forwarded message for admins
    forward_msg = (
        f"📦 *New Order Message*\n\n"
        f"👤 *From:* {user.first_name} {user.last_name or ''}\n"
        f"🔗 *Username:* @{user.username or 'no username'}\n"
        f"🆔 *User ID:* `{user.id}`\n\n"
        f"💬 *Message:*\n{text}"
    )

    # Send to all admins
    for admin_id in ADMIN_IDS:
        try:
            await context.bot.send_message(
                chat_id=admin_id,
                text=forward_msg,
                parse_mode="Markdown"
            )
        except Exception as e:
            logging.error(f"Could not send to admin {admin_id}: {e}")

    # Auto reply to customer
    await update.message.reply_text(
        "✅ Thank you! Your message has been received.\n\n"
        "We will get back to you within 24 hours 🌿\n\n"
        "— GlowStack Team ✦"
    )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    caption = update.message.caption or "No caption"

    forward_msg = (
        f"📦 *New Order — Photo received*\n\n"
        f"👤 *From:* {user.first_name} {user.last_name or ''}\n"
        f"🔗 *Username:* @{user.username or 'no username'}\n"
        f"🆔 *User ID:* `{user.id}`\n\n"
        f"📎 *Caption:* {caption}"
    )

    for admin_id in ADMIN_IDS:
        try:
            await context.bot.send_photo(
                chat_id=admin_id,
                photo=update.message.photo[-1].file_id,
                caption=forward_msg,
                parse_mode="Markdown"
            )
        except Exception as e:
            logging.error(f"Could not send photo to admin {admin_id}: {e}")

    await update.message.reply_text(
        "✅ Thank you! Your message has been received.\n\n"
        "We will get back to you within 24 hours 🌿\n\n"
        "— GlowStack Team ✦"
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.run_polling()

if __name__ == "__main__":
    main()
