import os
import logging

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

USER_SETTINGS = {}


def get_settings(user_id):
    if user_id not in USER_SETTINGS:
        USER_SETTINGS[user_id] = {
            "market": "OTC",
            "timeframe": "1 MIN",
            "auto_scan": False
        }
    return USER_SETTINGS[user_id]


def main_menu(user_id):
    settings = get_settings(user_id)

    keyboard = [
        [
            InlineKeyboardButton("OTC MARKET", callback_data="market_otc"),
            InlineKeyboardButton("NORMAL MARKET", callback_data="market_normal")
        ],
        [
            InlineKeyboardButton("5 SEC", callback_data="tf_5s"),
            InlineKeyboardButton("30 SEC", callback_data="tf_30s")
        ],
        [
            InlineKeyboardButton("1 MIN", callback_data="tf_1m"),
            InlineKeyboardButton("5 MIN", callback_data="tf_5m")
        ],
        [
            InlineKeyboardButton(
                "AUTO SCANNER: " + ("ON 🟢" if settings["auto_scan"] else "OFF 🔴"),
                callback_data="auto_toggle"
            )
        ],
        [
            InlineKeyboardButton("GET SIGNAL 📊", callback_data="get_signal")
        ],
        [
            InlineKeyboardButton("MARKET ANALYSIS 🔍", callback_data="analysis"),
            InlineKeyboardButton("PERFORMANCE 📈", callback_data="performance")
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    settings = get_settings(user_id)

    message = (
        "🔥 SHARPSHUTRA AI PRO\n\n"
        "Welcome to Hybrid AI Trading System!\n\n"
        "🟢 TELEGRAM BOT: ONLINE\n"
        "🟡 MARKET DATA: NOT CONNECTED\n\n"
        f"📊 MARKET: {settings['market']}\n"
        f"⏱️ TIMEFRAME: {settings['timeframe']}\n\n"
        "Select your trading settings below.\n\n"
        "⚠️ Demo system. No verified live signals yet."
    )

    await update.message.reply_text(
        message,
        reply_markup=main_menu(user_id)
    )


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    settings = get_settings(user_id)
    action = query.data

    if action == "market_otc":
        settings["market"] = "OTC"

    elif action == "market_normal":
        settings["market"] = "NORMAL"

    elif action.startswith("tf_"):
        timeframes = {
            "tf_5s": "5 SECONDS",
            "tf_30s": "30 SECONDS",
            "tf_1m": "1 MINUTE",
            "tf_5m": "5 MINUTES"
        }
        settings["timeframe"] = timeframes[action]

    elif action == "auto_toggle":
        settings["auto_scan"] = not settings["auto_scan"]

        await query.edit_message_text(
            "🤖 AUTO SCANNER\n\n"
            + ("🟢 ON" if settings["auto_scan"] else "🔴 OFF")
            + "\n\nNote: Live market scanning is not connected yet.",
            reply_markup=main_menu(user_id)
        )
        return

    elif action == "get_signal":
        await query.edit_message_text(
            "🔥 SHARPSHUTRA AI PRO\n\n"
            "📊 MARKET: " + settings["market"] + "\n"
            "⏱️ TIMEFRAME: " + settings["timeframe"] + "\n\n"
            "⚠️ No verified signal available.\n"
            "Market data connection is required before "
            "CALL/PUT analysis can be generated.",
            reply_markup=main_menu(user_id)
        )
        return

    elif action == "analysis":
        await query.edit_message_text(
            "🔍 MARKET ANALYSIS\n\n"
            "Market: " + settings["market"] + "\n"
            "Timeframe: " + settings["timeframe"] + "\n\n"
            "RSI: Waiting for market data\n"
            "EMA: Waiting for market data\n"
            "MACD: Waiting for market data\n"
            "PRICE ACTION: Waiting for market data\n\n"
            "🟡 Data feed not connected.",
            reply_markup=main_menu(user_id)
        )
        return

    elif action == "performance":
        await query.edit_message_text(
            "📈 SHARPSHUTRA PERFORMANCE\n\n"
            "Verified trades: 0\n"
            "Win rate: Not available\n"
            "Loss rate: Not available\n\n"
            "Performance statistics will appear "
            "after verified signal testing.",
            reply_markup=main_menu(user_id)
        )
        return

    await query.edit_message_text(
        "🔥 SHARPSHUTRA AI PRO\n\n"
        "🟢 Settings updated!\n\n"
        "Market: " + settings["market"] + "\n"
        "Timeframe: " + settings["timeframe"],
        reply_markup=main_menu(user_id)
    )


def main():
    if not TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN missing")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CallbackQueryHandler(buttons))

    print("SHARPSHUTRA AI PRO ONLINE")

    app.run_polling()


if __name__ == "__main__":
    main()
