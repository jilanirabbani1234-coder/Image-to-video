import os
import glob
import logging
import asyncio

logger = logging.getLogger(__name__)
BASE_TMP = os.path.join("bot_workdir", "tmp")
os.makedirs(BASE_TMP, exist_ok=True)

async def download_message_media(message, file_type="photo") -> str:
    """
    Downloads media to tmp and returns local path.
    message: pyrogram Message
    file_type: 'photo' or 'document'
    """
    # pyrogram message.download returns path
    # Use the highest quality photo
    path = await message.download(file_name=os.path.join(BASE_TMP, f"input_{message.message_id}"))
    return path

def cleanup_files(older_than_seconds: int = 60 * 60):
    """
    Cleans up tmp files older than `older_than_seconds` to save disk.
    """
    import time
    now = time.time()
    patterns = [os.path.join(BASE_TMP, "*")]
    removed = 0
    for pattern in patterns:
        for f in glob.glob(pattern):
            try:
                if os.path.isfile(f):
                    mtime = os.path.getmtime(f)
                    if now - mtime > older_than_seconds:
                        os.remove(f)
                        removed += 1
            except Exception:
                logger.exception("cleanup failed for %s", f)
    logger.debug("cleanup removed %d files", removed)
