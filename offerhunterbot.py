import html
import os
from dotenv import load_dotenv
import telebot
from scrapper import search_offers
from programathor_scrapper import search_offers_programathor

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def greetings(message):
    name = html.escape(message.from_user.first_name or "there")
    welcome = (
        f"Hey {name}! 👋\n\n"
        "I'm your <b>job-scout bot</b> still bootstrapping, but here's the plan:\n"
        "track openings with AI, bundle them up, and ping you with "
        "<b>clean, formatted digests</b> so you skip the noise.\n\n"
        "Try typing <code>vagas</code> for a quick teaser."
    )
    bot.reply_to(message, welcome, parse_mode="HTML")

@bot.message_handler(func=lambda message: True)
def listener(message):
    text = message.text.lower()

    user_name = message.from_user.first_name
    id_user = message.chat.id
    original_text = message.text

    print(f"[LOG] {user_name} (ID: {id_user}): (ENVIOU: {original_text})")

    if str(id_user) != ADMIN_ID:
        alert = f"*Alerta de Uso*\n👤 Usuário: {user_name} \n Mensagem: {original_text}"
        bot.send_message(ADMIN_ID, alert, parse_mode="Markdown")

    match text:
        case "programathor":
            bot.reply_to(message, "Iniciando busca de vagas em programathor...")
            try:
                result = search_offers_programathor()
            except Exception:
                result = "⚠️ Erro interno ao processar a busca. Tente novamente."
                
            bot.reply_to(message, result, parse_mode="HTML", disable_web_page_preview=True)
        case _:
            bot.reply_to(message, "Comando não identificado")

bot.infinity_polling()