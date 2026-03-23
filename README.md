# Offer Hunter

Early-stage Telegram bot in Python. Planned evolution: AI-assisted job discovery, aggregation, and formatted vacancy digests delivered to you.

---

## Current features

- `/start` command — welcome message in English (personalized, HTML formatting).
- Every other message is logged to the console.
- If the sender is **not** the configured administrator, the bot sends an **alert** to the admin with the user’s name and message text.
- Sample keywords (input is lowercased with `lower()`):
  - `vagas` → fixed reply (*Sem vagas*)
  - anything else → *Comando não identificado*

## Roadmap

- Plug in job sources (APIs, feeds, etc., respecting each provider’s terms).
- Use AI to extract and normalize fields (company, role, location, link, deadline).
- Deliver **one channel** of **clean, formatted** digests instead of raw noise.

## Requirements

- Python 3.10+ (the code uses `match` / `case`).
- A [BotFather](https://t.me/BotFather) token for your bot.

## Setup

1. Clone the repository and `cd` into the project folder.

2. Create and activate a virtual environment (recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Linux/macOS
   # Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install pyTelegramBotAPI python-dotenv
   ```

4. Create a `.env` file in the project root **(do not commit this file)**:

   ```env
   TELEGRAM_TOKEN=your_botfather_token
   ADMIN_ID=your_numeric_chat_id
   ```

   `ADMIN_ID` is the admin’s numeric Telegram user ID (same shape as `message.chat.id`). Only that user is skipped for “usage alert” messages when talking to the bot.

## Run

```bash
python offerhunterbot.py
```

The bot uses long polling (`infinity_polling()`); keep the process running while you want the bot online.

## Security

- Never commit `.env` or tokens to Git.
- If a token leaks, revoke it in BotFather and issue a new one.


