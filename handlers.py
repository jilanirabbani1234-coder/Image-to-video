import os
import logging
import tempfile
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyrogram import Client
from api_client import send_image_for_generation, send_text_for_generation
from utils import download_message_media, cleanup_files

logger = logging.getLogger(__name__)

# Allowed durations (seconds)
ALLOWED_DURATIONS = [3, 4, 5, 6]

def register_handlers(app: Client):
    @app.on_message(filters.command("start") & filters.private)
    async def start_cmd(client: Client, message: Message):
        await message.reply_text(
            "Salam! Main Image->Video aur Prompt->Video bot hoon.\n\n"
            "Send a photo to convert to a 3-6s video.\n"
            "Or send a text prompt and I will make a short 3-6s video.\n\n"
            "Commands:\n"
            "/dur X - set duration in seconds (3-6). Default 5.\n"
            "/help - this message."
        )
        # set default duration in chat data (we use temp file approach)
        # You can implement persistent storage if needed.

    @app.on_message(filters.command("help") & filters.private)
    async def help_cmd(client: Client, message: Message):
        await message.reply_text("Just send a photo or a prompt text. Use /dur X to choose duration (3-6).")

    @app.on_message(filters.command("dur") & filters.private)
    async def dur_cmd(client: Client, message: Message):
        try:
            arg = int(message.text.split()[1])
            if arg not in ALLOWED_DURATIONS:
                raise ValueError()
            # store as file in temp directory keyed by chat id
            cfg_dir = os.path.join("bot_workdir", "chat_cfg")
            os.makedirs(cfg_dir, exist_ok=True)
            with open(os.path.join(cfg_dir, f"{message.chat.id}.dur"), "w") as f:
                f.write(str(arg))
            await message.reply_text(f"Duration set to {arg} seconds.")
        except Exception:
            await message.reply_text("Usage: /dur X  (where X is 3,4,5 or 6)")

    @app.on_message(filters.photo & filters.private)
    async def photo_handler(client: Client, message: Message):
        chat_id = message.chat.id
        # get duration if set
        cfg_dir = os.path.join("bot_workdir", "chat_cfg")
        dur = 5
        try:
            with open(os.path.join(cfg_dir, f"{chat_id}.dur"), "r") as f:
                dur = int(f.read().strip())
        except Exception:
            dur = 5

        await message.reply_text("Photo received. Generating short video... (this may take a few seconds)")

        try:
            input_path = await download_message_media(message, file_type="photo")
            # call colab API
            result = send_image_for_generation(input_path, duration=dur)
            if not result or "error" in result:
                await message.reply_text("Error: failed to generate video.")
                return

            video_path = result.get("video_path")
            # send video
            await client.send_video(chat_id, video_path, caption=f"Here's your {dur}s video.")
        except FloodWait as e:
            logger.warning(f"FloodWait: sleeping {e.x}s")
            await asyncio.sleep(e.x)
            await message.reply_text("Retrying after wait...")
        except Exception as e:
            logger.exception("Failed to process photo")
            await message.reply_text(f"Error: {e}")
        finally:
            cleanup_files()

    @app.on_message(filters.text & ~filters.command & filters.private)
    async def text_handler(client: Client, message: Message):
        chat_id = message.chat.id
        prompt = message.text.strip()
        if len(prompt) < 3:
            await message.reply_text("Prompt too short. Send a longer description.")
            return

        # get duration
        cfg_dir = os.path.join("bot_workdir", "chat_cfg")
        dur = 5
        try:
            with open(os.path.join(cfg_dir, f"{chat_id}.dur"), "r") as f:
                dur = int(f.read().strip())
        except Exception:
            dur = 5

        await message.reply_text("Prompt received. Generating short video... (this may take several seconds)")

        try:
            result = send_text_for_generation(prompt, duration=dur)
            if not result or "error" in result:
                await message.reply_text("Error: failed to generate video.")
                return
            video_path = result.get("video_path")
            await client.send_video(chat_id, video_path, caption=f"Here's your {dur}s video for the prompt.")
        except Exception as e:
            logger.exception("Failed to process prompt")
            await message.reply_text(f"Error: {e}")
        finally:
            cleanup_files()
