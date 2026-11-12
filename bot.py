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

# 20 CURRENCY PAIRS
CURRENCY_PAIRS = [
    "EUR/USD",
    "GBP/USD",
    "USD/JPY",
    "AUD/USD",
    "USD/CAD",
    "USD/CHF",
    "NZD/USD",
    "EUR/GBP",
    "EUR/JPY",
    "EUR/AUD",
    "GBP/JPY",
    "GBP/AUD",
    "GBP/CAD",
    "AUD/JPY",
    "AUD/CAD",
    "CAD/JPY",
    "CHF/JPY",
    "EUR/CAD",
    "EUR/CHF",
    "NZD/JPY"
]


def get_settings(user_id):
    if user_id not in USER_SETTINGS:
        USER_SETTINGS[user_id] = {
            "market": "OTC",
            "timeframe": "1 MINUTE",
            "pair": "EUR/USD",
            "auto_scan": False
        }

    return USER_SETTINGS[user_id]


def main_menu(user_id):

    settings = get_settings(user_id)

    keyboard = [
        [
            InlineKeyboardButton(
                "OTC MARKET",
                callback_data="market_otc"
            ),
            InlineKeyboardButton(
                "NORMAL MARKET",
                callback_data="market_normal"
            )
        ],
        [
            InlineKeyboardButton(
                "CURRENCY PAIR 💱",
                callback_data="pair_menu"
            )
        ],
        [
            InlineKeyboardButton(
                "5 SEC",
                callback_data="tf_5s"
            ),
            InlineKeyboardButton(
                "30 SEC",
                callback_data="tf_30s"
            )
        ],
        [
            InlineKeyboardButton(
                "1 MIN",
                callback_data="tf_1m"
            ),
            InlineKeyboardButton(
                "5 MIN",
                callback_data="tf_5m"
            )
        ],
        [
            InlineKeyboardButton(
                "AUTO SCANNER: "
                + ("ON 🟢" if settings["auto_scan"] else "OFF 🔴"),
                callback_data="auto_toggle"
            )
        ],
        [
            InlineKeyboardButton(
                "GET SIGNAL 📊",
                callback_data="get_signal"
            )
        ],
        [
            InlineKeyboardButton(
                "MARKET ANALYSIS 🔍",
                callback_data="analysis"
            ),
            InlineKeyboardButton(
                "PERFORMANCE 📈",
                callback_data="performance"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


def pair_menu():

    keyboard = []

    # Two currency pairs per row
    for i in range(0, len(CURRENCY_PAIRS), 2):

        row = [
            InlineKeyboardButton(
                CURRENCY_PAIRS[i],
                callback_data="pair_" + CURRENCY_PAIRS[i].replace("/", "_")
            ),
            InlineKeyboardButton(
                CURRENCY_PAIRS[i + 1],
                callback_data="pair_" + CURRENCY_PAIRS[i + 1].replace("/", "_")
            )
        ]

        keyboard.append(row)

    keyboard.append([
        InlineKeyboardButton(
            "⬅️ BACK TO DASHBOARD",
            callback_data="back_menu"
        )
    ])

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
        f"💱 PAIR: {settings['pair']}\n"
        f"⏱️ TIMEFRAME: {settings['timeframe']}\n\n"
        "Select your trading settings below.\n\n"
        "⚠️ No verified live signals yet."
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

    # MARKET SELECTION

    if action == "market_otc":

        settings["market"] = "OTC"

    elif action == "market_normal":

        settings["market"] = "NORMAL"

    # TIMEFRAME SELECTION

    elif action.startswith("tf_"):

        timeframes = {
            "tf_5s": "5 SECONDS",
            "tf_30s": "30 SECONDS",
            "tf_1m": "1 MINUTE",
            "tf_5m": "5 MINUTES"
        }

        settings["timeframe"] = timeframes[action]

    # OPEN CURRENCY PAIR MENU

    elif action == "pair_menu":

        await query.edit_message_text(
            "💱 SHARPSHUTRA AI PRO\n\n"
            "SELECT CURRENCY PAIR\n\n"
            f"Current Pair: {settings['pair']}\n\n"
            "Choose your preferred currency pair:",
            reply_markup=pair_menu()
        )

        return

    # SELECT CURRENCY PAIR

    elif action.startswith("pair_"):

        selected_pair = action.replace(
            "pair_", ""
        ).replace("_", "/")

        if selected_pair in CURRENCY_PAIRS:

            settings["pair"] = selected_pair

        await query.edit_message_text(
            "🟢 CURRENCY PAIR UPDATED!\n\n"
            f"Selected Pair: {settings['pair']}\n"
            f"Market: {settings['market']}\n"
            f"Timeframe: {settings['timeframe']}\n\n"
            "Your settings have been updated.",
            reply_markup=main_menu(user_id)
        )

        return

    # BACK TO DASHBOARD

    elif action == "back_menu":

        await query.edit_message_text(
            "🔥 SHARPSHUTRA AI PRO\n\n"
            f"📊 MARKET: {settings['market']}\n"
            f"💱 PAIR: {settings['pair']}\n"
            f"⏱️ TIMEFRAME: {settings['timeframe']}\n\n"
            "Select your trading settings.",
            reply_markup=main_menu(user_id)
        )

        return

    # AUTO SCANNER

    elif action == "auto_toggle":

        settings["auto_scan"] = not settings["auto_scan"]

        await query.edit_message_text(
            "🤖 AUTO SCANNER\n\n"
            + ("🟢 ON" if settings["auto_scan"] else "🔴 OFF")
            + "\n\n"
            "Note: Live market scanning is not connected yet.",
            reply_markup=main_menu(user_id)
        )

        return

    # GET SIGNAL

    elif action == "get_signal":

        import os
        import requests

        api_key = os.getenv("OTCHARTS_API_KEY")

        if not api_key:
            await query.edit_message_text(
                "❌ OTCHARTS API KEY NOT FOUND.",
                reply_markup=main_menu(user_id)
            )
            return

        symbol = settings["pair"]

        if settings["market"] == "OTC" and not symbol.endswith("_otc"):
            symbol = symbol.replace("/", "") + "_otc"

        timeframe = settings["timeframe"]

        tf_map = {
            "5s": 5,
            "30s": 30,
            "1m": 60,
            "5m": 300
        }

        tf = tf_map.get(timeframe, 60)

        await query.edit_message_text("⏳ Fetching market data...")

        try:
            response = requests.get(
                "https://otcharts.com/v1/candles",
                headers={
                    "Authorization": f"Bearer {api_key}"
                },
                params={
                    "venue": "otc",
                    "symbol": symbol,
                    "tf": tf,
                    "limit": 50
                },
                timeout=15
            )

            if response.status_code != 200:
                raise Exception(
                    f"API error: HTTP {response.status_code}"
                )

            data = response.json()
            candles = data.get("candles", [])

            if len(candles) < 20:
                raise Exception("Not enough candle data")

            await query.edit_message_text(
                "✅ MARKET DATA RECEIVED\n\n"
                f"Pair: {symbol}\n"
                f"Timeframe: {timeframe}\n"
                f"Candles received: {len(candles)}\n\n"
                "⚠️ Signal engine is not connected yet.",
                reply_markup=main_menu(user_id)
            )

        except Exception as e:
            await query.edit_message_text(
                "❌ MARKET DATA ERROR\n\n"
                f"{str(e)[:250]}",
                reply_markup=main_menu(user_id)
            )

        return


    # MARKET ANALYSIS

    elif action == "analysis":

        await query.edit_message_text(
            "🔍 MARKET ANALYSIS\n\n"
            f"Market: {settings['market']}\n"
            f"Pair: {settings['pair']}\n"
            f"Timeframe: {settings['timeframe']}\n\n"
            "RSI: Waiting for market data\n"
            "EMA: Waiting for market data\n"
            "MACD: Waiting for market data\n"
            "Bollinger Bands: Waiting for market data\n"
            "PRICE ACTION: Waiting for market data\n\n"
            "🟡 DATA FEED NOT CONNECTED.",
            reply_markup=main_menu(user_id)
        )

        return

    # PERFORMANCE

    elif action == "performance":

        await query.edit_message_text(
            "📈 SHARPSHUTRA PERFORMANCE\n\n"
            "Verified trades: 0\n"
            "Win rate: Not available\n"
            "Loss rate: Not available\n\n"
            "Statistics will appear after verified testing.",
            reply_markup=main_menu(user_id)
        )

        return

    # UPDATE DASHBOARD

    await query.edit_message_text(
        "🔥 SHARPSHUTRA AI PRO\n\n"
        "🟢 SETTINGS UPDATED!\n\n"
        f"Market: {settings['market']}\n"
        f"Pair: {settings['pair']}\n"
        f"Timeframe: {settings['timeframe']}",
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
