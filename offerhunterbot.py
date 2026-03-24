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
        f"Olá, {name}! 👋\n\n"
        "Bem-vindo ao <b>Offer Hunter</b>.\n"
        "Posso buscar vagas de tecnologia e te enviar tudo em um formato organizado.\n\n"
        "Digite <code>programathor</code> para iniciar a busca agora.\n"
        "Digite <code>help</code> a qualquer momento para ver os comandos disponíveis."
    )
    bot.reply_to(message, welcome, parse_mode="HTML")


@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = (
        "<b>Comandos disponíveis</b>\n\n"
        "/start - Mensagem de boas-vindas\n"
        "Também posso responder ao texto <code>programathor</code> para buscar vagas."
    )
    bot.reply_to(message, help_text, parse_mode="HTML")

@bot.message_handler(commands=['programathor'])
def programathor_command(message):
    bot.reply_to(message, "Iniciando busca de vagas em programathor...")
    try:
        result = search_offers_programathor()
    except Exception:
        result = "⚠️ Erro interno ao processar a busca. Tente novamente."
    bot.reply_to(message, result, parse_mode="HTML", disable_web_page_preview=True)


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
        case _:
            bot.reply_to(message, "Comando não identificado")

bot.infinity_polling()