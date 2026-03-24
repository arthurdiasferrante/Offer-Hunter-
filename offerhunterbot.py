import html
import os
import time

from dotenv import load_dotenv
import telebot
from scrapper import search_offers
from programathor_scrapper import set_page_range

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
bot = telebot.TeleBot(TOKEN)


# Mensagem de boas vindas
@bot.message_handler(commands=['start'])
def greetings(message):
    name = html.escape(message.from_user.first_name or "there")
    welcome = (
        f"Olá, {name}! 👋\n\n"
        "Bem-vindo ao <b>Offer Hunter</b>.\n"
        "Posso buscar vagas de tecnologia e te enviar tudo em um formato organizado.\n\n"
        "Digite <code>programathor</code> para iniciar a busca agora.\n"
        "Digite <code>help</code> a qualquer momento para ver os comandos disponíveis."
    )
    bot.reply_to(message, welcome, parse_mode="HTML")


# Mensagem de ajuda
@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = (
        "<b>Comandos disponíveis</b>\n\n"
        "🚀 <b>/start</b>\n"
        "Mostra a mensagem de boas-vindas.\n\n"
        "🔎 <b>/programathor</b>\n"
        "Busca vagas no Programathor e retorna os resultados formatados.\n\n"
        "❓ <b>/help</b>\n"
        "Exibe este guia.\n\n"
        "<b>Atalhos sem barra:</b>\n"
        "Você também pode enviar <code>programathor</code> ou <code>help</code>."
    )
    bot.reply_to(message, help_text, parse_mode="HTML")

# Procura vagas no site "Programathor.com"
@bot.message_handler(commands=['programathor'])
def programathor_command(message):
    msg = bot.reply_to(message, "De qual a qual página você quer ir? (Ex: 1-5)")
    bot.register_next_step_handler(msg, process_page_range)

def process_page_range(message):
    user_text = message.text

    try:
        parts = user_text.split("-")
        initial_page = int(parts[0].strip())
        last_page = int(parts[1].strip())

        bot.reply_to(message, f"Iniciando busca de {initial_page} até {last_page}")

        result = set_page_range(initial_page, last_page)

        if isinstance(result, list):
            for pacote in result:
                bot.reply_to(message, pacote, parse_mode="HTML", disable_web_page_preview=True)
                time.sleep(1)
        elif result:
            bot.reply_to(message, result, parse_mode="HTML", disable_web_page_preview=True)

    except (ValueError, IndexError):
        bot.reply_to(message, "⚠️ Formato inválido. O processo foi cancelado. Digite programathor novamente e use o formato '1-5'.")

# Lida com mensagens soltas (sem slash /)
@bot.message_handler(func=lambda message: True)
def listener(message):
    text = message.text.lower().strip()

    user_name = message.from_user.first_name
    id_user = message.chat.id
    original_text = message.text

    print(f"[LOG] {user_name} (ID: {id_user}): (ENVIOU: {original_text})")

    if str(id_user) != ADMIN_ID:
        alert = f"*Alerta de Uso*\n👤 Usuário: {user_name} \n Mensagem: {original_text}"
        bot.send_message(ADMIN_ID, alert, parse_mode="Markdown")

    match text:
        case "help":
            help_command(message)
        case "programathor":
            programathor_command(message)
        case _:
            bot.reply_to(
                message,
                "Comando não identificado. Use <code>/help</code> para ver os comandos.",
                parse_mode="HTML"
            )

bot.infinity_polling()