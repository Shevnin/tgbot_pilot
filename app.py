from flask import Flask, request
import telebot
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os
import json

TOKEN = os.environ.get("8086575089:AAGXMAx58w8fHhCxv_MXM71JuwjsZ-umKrE") or 'сюда_твой_токен'
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Google Sheets авторизация
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(os.environ.get("GOOGLE_CREDS"))
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open("FocusTracker").sheet1

# Обработка сообщений
@bot.message_handler(func=lambda message: True)
def handle_all(message):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    sheet.append_row([now, message.from_user.first_name, message.text])
    bot.reply_to(message, "✅ Записал в таблицу!")

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "ok", 200

@app.route("/")
def index():
    return "Бот работает!"

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"https://tgbot-pilot.onrender.com/{TOKEN}")
    app.run(host="0.0.0.0", port=5000)