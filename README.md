# Offer Hunter

Telegram bot in Python focused on job hunting automation.  
Today it scrapes Programathor jobs and sends filtered results to Telegram.  
The long-term goal is to evolve into an AI-assisted job discovery and formatting assistant.

---

## What it does today

- Handles `/start` with a welcome message.
- Logs incoming messages in the terminal.
- Sends a usage alert to the admin when a non-admin user interacts with the bot.
- Supports command-like keyword handling:
  - `programathor` -> starts a scraping search and returns formatted job results.
  - anything else -> `Comando não identificado`.

## How `programathor` works

When the user sends `programathor`, the bot:

1. Scrapes jobs from `https://programathor.com.br/jobs`.
2. Stops scanning when it reaches expired jobs (`color-gray` marker in title block).
3. Filters by location.
4. Formats matches as a Telegram message with title, location, and link.

If nothing matches, it returns `❌ Nenhuma vaga encontrada com esses filtros no momento`.

## Project structure

- `offerhunterbot.py` -> Telegram bot handlers, admin alerts, polling loop.
- `programathor_scrapper.py` -> Programathor scraping and filtering logic (`search_offers_programathor()`).
- `scrapper.py` -> legacy/experimental scraper module.

## Requirements

- Python 3.10+ (the bot uses `match` / `case`).
- A Telegram bot token from [BotFather](https://t.me/BotFather).

## Setup

1. Clone the repository and enter the project folder.
2. Create and activate a virtual environment (recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Linux/macOS
   # Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   `requirements.txt` contains pinned versions used by the project.

4. Create a `.env` file in the project root (do not commit this file):

   ```env
   TELEGRAM_TOKEN=your_botfather_token
   ADMIN_ID=your_numeric_chat_id
   ```

`ADMIN_ID` must be your numeric Telegram user/chat ID (same format used by `message.chat.id`).

## Run

```bash
python offerhunterbot.py
```

The bot uses long polling (`infinity_polling()`), so keep the process running while the bot is online.

## Roadmap

- Add more real job sources (APIs and/or compliant scraping targets).
- Improve filters by skills, role type, location, and seniority.
- Introduce AI-powered ranking and cleaner digest formatting.

## Security

- Never commit `.env` or bot tokens.
- If a token leaks, revoke and regenerate it in BotFather.


