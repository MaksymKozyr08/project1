# Telegram UserBot (Pyrogram)

UserBot for a personal Telegram account (not BotFather bot).

## What it does

- Monitors incoming text messages in private chats and groups
- Ignores your own messages
- Checks if message contains `?`
- Extracts number at the very start of the message
- Replies to that message with only the extracted number
- Adds random delay `0.5 - 1.5` sec before reply

## Setup

1. Open `main.py`
2. Set:
   - `api_id`
   - `api_hash`

## Install

```bash
pip install -r requirements.txt
```

## First run

```bash
python main.py
```

On first run you will enter:
- phone number
- Telegram login code
- 2FA password (if enabled)

After login, session file is created (`my_userbot.session`) and reused later.
