import os
import requests
import uuid
import time
from config.config import COLAB_API_URL, COLAB_API_KEY  # Put API URL (ngrok/colab link) and optional key if set

TMP_DIR = os.path.join("bot_workdir", "tmp")
os.makedirs(TMP_DIR, exist_ok=True)

def _save_streamed_file(resp, filename):
    path = os.path.join(TMP_DIR, filename)
    with open(path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    return path

def send_image_for_generation(image_path: str, duration: int = 5) -> dict:
    """
    Sends image to the colab API and downloads generated video.
    Returns dict: { "video_path": local_path } or {"error": "msg"}
    """
    url = COLAB_API_URL.rstrip("/") + "/generate"
    files = {"file": open(image_path, "rb")}
    data = {"type": "image", "duration": str(duration)}
    headers = {}
    if COLAB_API_KEY:
        headers["x-api-key"] = COLAB_API_KEY

    try:
        resp = requests.post(url, files=files, data=data, headers=headers, stream=True, timeout=300)
        if resp.status_code != 200:
            return {"error": f"API error {resp.status_code} {resp.text}"}
        # Response is a streamed video file
        filename = f"video_{int(time.time())}_{uuid.uuid4().hex[:6]}.mp4"
        path = _save_streamed_file(resp, filename)
        return {"video_path": path}
    except Exception as e:
        return {"error": str(e)}

def send_text_for_generation(prompt: str, duration: int = 5) -> dict:
    url = COLAB_API_URL.rstrip("/") + "/generate"
    data = {"type": "text", "prompt": prompt, "duration": str(duration)}
    headers = {}
    if COLAB_API_KEY:
        headers["x-api-key"] = COLAB_API_KEY

    try:
        resp = requests.post(url, json=data, headers=headers, stream=True, timeout=300)
        if resp.status_code != 200:
            return {"error": f"API error {resp.status_code} {resp.text}"}
        filename = f"video_{int(time.time())}_{uuid.uuid4().hex[:6]}.mp4"
        path = _save_streamed_file(resp, filename)
        return {"video_path": path}
    except Exception as e:
        return {"error": str(e)}
