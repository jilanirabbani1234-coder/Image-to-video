import logging
import asyncio
from pyrogram import Client
from config.config import BOT_TOKEN, API_ID, API_HASH
from handlers import register_handlers

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

# Pyrogram requires API_ID and API_HASH (create from my.telegram.org) OR use Bot token only with bot token init
# We will use bot token mode with session name "video_ai_bot"
APP_NAME = "video_ai_bot"

def main():
    logger.info("Starting Telegram Video-AI Bot...")
    app = Client(
        APP_NAME,
        bot_token=BOT_TOKEN,
        api_id=API_ID,
        api_hash=API_HASH,
        workdir="./bot_workdir"
    )

    # register message handlers (from handlers.py)
    register_handlers(app)

    # run bot
    app.run()

if __name__ == "__main__":
    main()
