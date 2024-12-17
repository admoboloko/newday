import os
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
import requests

# Bot Token (set as an environment variable on Render)
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Port for Render (Render provides this dynamically)
PORT = int(os.environ.get("PORT", 5000))

# Initialize Flask app
app = Flask(__name__)

# Initialize Telegram bot
application = ApplicationBuilder().token(TOKEN).build()

# Start command handler
async def start(update: Update, context: CallbackContext):
    user = update.effective_user
    username = user.username or user.first_name

    welcome_photo_url = "https://imgur.com/aDHfR5m"
    await update.message.reply_photo(
        photo=welcome_photo_url,
        caption=f"👋 Welcome to BLDX TON Miner App, {username}! 🚀\nLet's get started on your mining journey."
    )

    await update.message.reply_photo(
        photo="https://imgur.com/a/6JUmXY9",
        caption="Get Ready, Get Set, Mine TON! 🚀⛏️💰\nStart your journey with **BLDX TON Miner** and unlock exciting rewards!",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Open BLDX Miner", url="https://t.me/BLDXTONbot")],
            [InlineKeyboardButton("Join Community", url="https://t.me/bldxtonminers")]
        ])
    )

# Add the command handler
application.add_handler(CommandHandler("start", start))

# Flask route for webhook
@app.post(f"/{TOKEN}")
async def webhook():
    """Receive updates from Telegram."""
    update = Update.de_json(request.json, application.bot)
    await application.process_update(update)
    return "OK", 200

# Set webhook automatically
@app.before_first_request
def set_webhook():
    """Tell Telegram where to send updates."""
    webhook_url = f"https://YOUR-RENDER-DOMAIN.onrender.com/{TOKEN}"
    requests.post(f"https://api.telegram.org/bot{TOKEN}/setWebhook", json={"url": webhook_url})

# Start Flask server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
