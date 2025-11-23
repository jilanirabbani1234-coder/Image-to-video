import os

# Telegram Bot token from BotFather
BOT_TOKEN = os.getenv("BOT_TOKEN", "PUT_YOUR_BOT_TOKEN_HERE")

# Pyrogram API ID/HASH (create at my.telegram.org) - optional but recommended
API_ID = int(os.getenv("API_ID", "1234567"))
API_HASH = os.getenv("API_HASH", "your_api_hash_here")

# The public URL where your Colab server is reachable (e.g. https://xxxx.ngrok.io)
COLAB_API_URL = os.getenv("COLAB_API_URL", "http://127.0.0.1:7860")

# optional API key to protect the endpoint (set same in server)
COLAB_API_KEY = os.getenv("COLAB_API_KEY", "")
