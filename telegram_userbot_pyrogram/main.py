import asyncio
import random
import re

from pyrogram import Client, filters
from pyrogram.types import Message

# =========================
# Telegram API credentials
# =========================
api_id = 30153177  # Replace with your real api_id (int)
api_hash = "67692d5210e81dcc77618d82c3136057"  # Replace with your real api_hash (str)

# Session name -> creates/uses local session file:
# "my_userbot.session"
session_name = "my_userbot"

app = Client(
    "my_userbot",  # Просто назва в лапках, без session_name=
    api_id=api_id,
    api_hash=api_hash
)

# Number at the very beginning (optional leading spaces)
START_NUMBER_RE = re.compile(r"^\s*(\d+)\b")


@app.on_message(filters.text & ~filters.me) 
async def auto_reply_number(client: Client, message: Message) -> None:
    try:
        text = message.text or ""

        # Process only messages with "?"
        if "?" not in text:
            return

        # Extract number from start
        match = START_NUMBER_RE.match(text)
        if not match:
            return

        extracted_number = match.group(1)

        # Human-like pause
        await asyncio.sleep(random.uniform(0.5, 1.5))

        # Reply to the same message
        await message.reply_text(extracted_number)
    except Exception as exc:
        # Basic error handling to keep script alive
        msg_id = getattr(message, "id", "unknown")
        print(f"[WARN] Failed to process message {msg_id}: {exc}")


if __name__ == "__main__":
    print("Starting Pyrogram UserBot...")
    app.run()
