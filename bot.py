import os
import time
import requests
from telegram import Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update

# ENV ayarları
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL_MINUTES", 15))
TARGET_PROFIT = float(os.getenv("TARGET_PROFIT_PERCENT", 2.0))
MAX_REMINDER = int(os.getenv("MAX_REMINDER_COUNT", 3))

bot = Bot(token=BOT_TOKEN)

# Geçici hafıza (RAM)
active_signals = {}

def get_mock_bist_data():
    """
    ŞİMDİLİK SAHTE VERİ
    Gerçek BIST verisini bir sonraki adımda bağlayacağız
    """
    return [
        {"symbol": "ASELS", "price": 58.20, "change": 1.3},
        {"symbol": "THYAO", "price": 276.50, "change": 2.1},
        {"symbol": "KCHOL", "price": 168.90, "change": 0.9},
    ]

async def taipo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = get_mock_bist_data()

    # En iyi 3 hisse (değişime göre)
    top3 = sorted(data, key=lambda x: x["change"], reverse=True)[:3]

    message = "📊 *TAIPO-BİST GÜN İÇİ RADAR*\n\n"

    for stock in top3:
        signal = "👀 İZLE"
        if stock["change"] >= TARGET_PROFIT:
            signal = "🟢 AL"

        message += (
            f"🔹 {stock['symbol']}\n"
            f"Fiyat: {stock['price']} TL\n"
            f"Değişim: %{stock['change']}\n"
            f"Sinyal: {signal}\n\n"
        )

    await update.message.reply_text(message, parse_mode="Markdown")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("taipo", taipo_command))
    print("TAIPO-BİST bot çalışıyor...")
    app.run_polling()

if __name__ == "__main__":
    main()
