import requests
import os
from dotenv import load_dotenv
import telebot

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def greetings (message):
    bot.reply_to(message, "Sistema online")

@bot.message_handler(func=lambda message: True)
def listener(message):
    text = message.text.lower()

    user_name = message.from_user.first_name
    id_user = message.chat.id
    original_text = message.text

    print(f"[LOG] {user_name} (ID: {id_user}): (ENVIOU: {original_text})")

    if str(id_user) != ADMIN_ID:
        alert = f"Alerta de Uso*\n👤 Usuário: {user_name} \n Mensagem: {original_text}"
        bot.send_message(ADMIN_ID, alert, parse_mode="Markdown")

    match text:
        case "banana":
            bot.reply_to(message, "oi banana")
        case "vagas":
            bot.reply_to(message, "Sem vagas")
        case _:
            bot.reply_to(message, "Comando não identificado")

bot.infinity_polling()