# Video-AI-Telegram-Bot (Hybrid)

Simple hybrid Telegram bot:
- Bot runs on a lightweight host (VPS / Render / Local).
- Heavy video generation runs on Colab (or GPU host) via FastAPI.

## Files
- `bot/` : Telegram bot code (pyrogram)
- `colab_api/` : server & notebook to run on Colab / GPU host
- `models/` : model wrapper stubs (replace with real pipelines)
- `config/config.py` : configure tokens & URLs
- `requirements.txt`

## Quick start (development)

1. Clone this repo.

2. Edit `config/config.py`:
   - Put your `BOT_TOKEN` (from BotFather).
   - Put `COLAB_API_URL` (the public URL of the Colab server; for local testing use http://127.0.0.1:7860)

3. Start the Colab server (on GPU machine / Colab):
   - Upload `colab_api/server.py` and `models/` folder to Colab.
   - Install dependencies (see comments in server.py).
   - Run: `uvicorn server:app --host 0.0.0.0 --port 7860`
   - Expose via ngrok or Colab tunneling to get a public URL.

4. Run the bot locally:
   - `pip install -r requirements.txt`
   - `python bot/bot.py`

5. Chat with the bot on Telegram:
   - Send a photo -> get short 3–6s video.
   - Send text -> get short 3–6s video.

## Deployment tips
- For stable hosting of the bot: use Render / Railway / small VPS.
- For model generation: use Colab Pro for more reliable GPU or a GPU VPS if you want continuous uptime.
- Protect your Colab endpoint with `COLAB_API_KEY` and check headers in server.py.

## Notes
- The `models/` functions are stubs for quick testing (they produce placeholder videos).
- Replace stubs with real video-diffusion pipelines (Stable Video Diffusion / ModelScope / Zeroscope).
- Keep secrets out of public repos (use environment variables / GH secrets).
