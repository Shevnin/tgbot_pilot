from flask import Flask, request
import telegram
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# ВСТАВЬ СЮДА СВОЙ ТОКЕН ОТ BotFather
TOKEN = '8086575089:AAGXMAx58w8fHhCxv_MXM71JuwjsZ-umKrE'

bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

# Авторизация Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("FocusTracker").sheet1

# Обработка сообщений от Telegram
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    text = update.message.text
    user = update.message.from_user.first_name
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    sheet.append_row([now, user, text])
    bot.send_message(chat_id=update.message.chat.id, text="✅ Записал в таблицу!")
    return 'ok'

# Страница-заглушка
@app.route('/')
def index():
    return 'Бот работает!'

if __name__ == "__main__":
    app.run(port=5000)