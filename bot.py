import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 WELCOME TO SHARPSHUTRA AI\n\n"
        "🤖 AI Trading Signal System\n"
        "📊 Platform: Pocket Option\n\n"
        "Commands:\n"
        "/signal - Get trading signal\n"
        "/status - Bot status\n"
    )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ SharpShutra Bot is ONLINE!"
    )


async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📊 SHARPSHUTRA AI\n\n"
        "Signal engine is being configured.\n"
        "No verified trading signal available yet."
    )


def main():
    if not TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN is missing")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("signal", signal))

    print("SharpShutra is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
