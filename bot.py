import telebot
import subprocess
import os
import requests
from telebot.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    LabeledPrice
)
import datetime
import gspread
from google.oauth2.service_account import Credentials

# === Ваші токени ===
TOKEN = '7721446505:AAEE0n__Qe-gLRCSqTJZfryc6R4b4I5UK_M'
PROVIDER_TOKEN = 'YOUR_PROVIDER_TOKEN'  # Отримати у @BotFather → /setpayment

# === Google Sheets ===
SPREADSHEET_ID = '1bMq4510saWiSeLfz-j9NINkHwATVrgBGuWL2EtPa4MU'  # ID таблиці (з URL)

INSTAGRAM_SESSIONID = '75681169834%3AFrxQy5b0jXmB69%3A28%3AAYd_3_K_B2YFi7jNbWO_RgFNAJBr7xPkwYYd03X2WA'
# SERVICE_ACCOUNT_INFO = {
#   "type": "service_account",
#   "project_id": "tg-prem-bot",
#   "private_key_id": "317f2a4a6baec86070c10a3fc7791477c8c908e1",
#   "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCQCtF4mY9IXKFh\ncVWHFTFtQT1rJ6tdCwsy/uSAvgMiTpxWjWH4hLD8rjqYg9wVqlxlxmRzTO4gD8M+\n5vOepNkDt9ouXvjws3Hd7K4iOLtUKsimuKDw71AZrC7ZmOQyPGzP3lQkGTw5+he8\nRSjSvPD2XHn8OMDl9lStztjj8PAmjVLZNARCRQeLwiT/LuPoaB6xeK0QAxE10Xih\nZJ6eWxthsCv9O/Hk1UwDBPUKM5dsotYBR+ugtT3bmkxD/i3Qpgv1cfApqXjEuJQM\njQxGzQCyB1ucWZY0z4DxqBlf+wL7ktRllz0POiHqLMzYAySmBSioZD6J7zI7U7U3\nlMN0d/LZAgMBAAECggEAQikV6cTusRgK8Az0ceVkHIC4yz0fUs89x6CYKCIeomVl\nHcQ22cVo3cbRFziJoFHturmTbfpJ7eQPlBbUk2u4WiLaTi5FPZnOlVae7Q0Nzi0Q\nmLN5CPGC4yfZJQ0603A5soi2MRZ+OUsMF+fURmeObjovtZAD2hx47JRzvs7uH2Zd\ntQE1sekzjHH1uvqfG7z7cf0aXQpK6FHADdrW6MvdKge37zLAjJoVdjukjmqSfkjL\n2cRGCiOWbxwyXOioZZHsEocs8kk3yi+isgMeYwPgWMaRAAltwxS3krB/hTAchEOp\nYvcvp4fs6eu6zCxxyZLzVmBF/8b+t1wQ7RxA4p0ceQKBgQDIXjUC+qJ5TKAjhwvs\n/hJ4u8ByThTzMjEKAbsCEywFlUynTQOIr3A2sNTyqd125+z9I0HeFZYQZJwrETRo\n44Eogsi1I9tg9O4CcLTBStdy0zKSwLzh3IKmq4AxUeHzKwqmMYIb0XQ4NDdxNukK\nKC0zTULNafyYRgZ8fftRNSvCdwKBgQC4CRSD5e246GRWtaeQjZoDhGbw+NQ/S5Xi\nKwZ9gXLDflg948kKDLRPVeLVXtR+tL/UhnYKbWS9JkfITQHRu2hU4EFhCsDTUnmd\nwY4Y0vLa7pLX3xy/qyEQ+sFOsGY7vsXxShqnBtaPkLQfeEmGQmiPTwYN8iJotvDL\nCsFqxeN5LwKBgDkWHiRrJD9LBZUZtNwgx0J+u6XVeUKQ2kfvlkhRDgnJL726w3b+\nBQqP9xvsKZznFy5IDUwo+khRYe0jSbtYlkPkfyqcvLQzFFy9n8IygI/GfHIzV51C\nJjc2RZ/HpIiTisUu9dLXKjWZKvKmol6yc65aJN5BhCYeTVrKyf+pFn6hAoGAfPPl\nUvy9YEuhPOJPqC0MghDWmAxKh8M5O/t8h6BpnGRfY34SVNl1X1xwC/E8E9+DU7gL\n016dBHRGTrBCaPV2jBJLMalMbO7VlhAB+8bWj2FmoF1jNpvpco7eyx+n+i64VPC8\nkeVprsZQFgHk4dybA5pjAPsC89gqO6HM20MLBI8CgYAym+u6QaRgWwGiq9C9eUXe\nOk/iyTz4mhTFOvsydquTSZ5U7Zy9H/Xw19Y1KYT/vSzy1epZYf9p9EoPzKI1OlOr\n9fRHBvllwiyBkcbtIFi7uWdFisfEL/2ftQ45phkDVdwmJ+GcQCzltmwnIZP+DCgx\n7qz26UBzad5BemT0+GZVBg==\n-----END PRIVATE KEY-----\n",
#   "client_email": "editor@tg-prem-bot.iam.gserviceaccount.com",
#   "client_id": "108474960811429249270",
#   "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#   "token_uri": "https://oauth2.googleapis.com/token",
#   "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#   "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/editor%40tg-prem-bot.iam.gserviceaccount.com",
#   "universe_domain": "googleapis.com"
# }

# Авторизація та підключення до таблиці
credentials = Credentials.from_service_account_info(
    SERVICE_ACCOUNT_INFO,
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
gc = gspread.authorize(credentials)
sheet = gc.open_by_key(SPREADSHEET_ID).sheet1

bot = telebot.TeleBot(TOKEN)

def is_premium(user_id):
    # Перевіряємо чи є користувач у Google Sheets і чи підписка активна
    records = sheet.get_all_records()
    now = datetime.datetime.utcnow()
    for rec in records:
        if int(rec['user_id']) == user_id:
            paid_date = datetime.datetime.strptime(rec['date'], "%Y-%m-%d")
            if (now - paid_date).days < 30:
                return True
    return False

def add_premium(user_id):
    # Додаємо або оновлюємо дату підписки для користувача
    records = sheet.get_all_records()
    now_str = datetime.datetime.utcnow().strftime("%Y-%m-%d")

    for idx, rec in enumerate(records, start=2):  # Починаючи з другого рядка (перший — заголовок)
        if int(rec['user_id']) == user_id:
            sheet.update_cell(idx, 2, now_str)  # Оновити дату
            return
    # Якщо немає користувача — додаємо новий рядок
    sheet.append_row([user_id, now_str])
    # --- Весь ваш код бота нижче (обробка команд, завантаження відео, оплати) ---

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message,
        "👋 Привіт! Надішли посилання на відео з:\n"
        "– YouTube 🎥\n– TikTok 🎵\n– Instagram 📸\n\n"
        "⚡️ Безкоштовно: до 720p\n💎 FullHD — після оплати через Telegram.\n"
        "Надішли посилання, і я все зроблю.")

@bot.message_handler(func=lambda m: True)
def handle_link(message):
    url = message.text.strip()
    user_id = message.chat.id

    if "youtube.com" in url or "youtu.be" in url:
        download_youtube(message, url, is_premium(user_id))
    elif "tiktok.com" in url:
        download_tiktok(message, url)
    elif "instagram.com" in url:
        download_instagram(message, url)
    else:
        bot.reply_to(message, "❗️ Непідтримуване посилання.")

def download_youtube(message, url, is_premium_user):
    quality = "best[height<=720]" if not is_premium_user else "bestvideo+bestaudio"
    note = "📥 Завантажую 720p..." if not is_premium_user else "📥 Завантажую FullHD..."

    bot.send_message(message.chat.id, note)
    filename = f"yt_{message.chat.id}.mp4"
    command = ["yt-dlp", "-f", quality, "-o", filename, url]

    try:
        subprocess.run(command, check=True)

        with open(filename, "rb") as video:
            markup = None
            if not is_premium_user:
                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton("💎 Отримати HD", callback_data="get_premium"))
            bot.send_video(message.chat.id, video, reply_markup=markup)

        os.remove(filename)

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Помилка: {e}")

def download_tiktok(message, url):
    bot.send_message(message.chat.id, "⏬ Завантажую з TikTok...")
    filename = f"tt_{message.chat.id}.mp4"
    command = ["yt-dlp", "-o", filename, url]
    try:
        subprocess.run(command, check=True)
        with open(filename, "rb") as video:
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("💎 Отримати HD", callback_data="get_premium"))
            bot.send_video(message.chat.id, video, reply_markup=markup)
        os.remove(filename)
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Помилка з TikTok: {e}")

def download_instagram(message, url):
    bot.send_message(message.chat.id, "⏬ Завантажую з Instagram...")

    filename = f"ig_{message.chat.id}.mp4"
    command = [
        "yt-dlp",
        "--add-header", f"Cookie: sessionid={INSTAGRAM_SESSIONID}",
        "-o", filename,
        url
    ]
    try:
        subprocess.run(command, check=True)
        with open(filename, "rb") as video:
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("💎 Отримати HD", callback_data="get_premium"))
            bot.send_video(message.chat.id, video, reply_markup=markup)
        os.remove(filename)
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Instagram помилка: {e}")

def send_external_video(chat_id, url):
    try:
        video = requests.get(url)
        with open("temp.mp4", "wb") as f:
            f.write(video.content)
        with open("temp.mp4", "rb") as f:
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("💎 Отримати HD", callback_data="get_premium"))
            bot.send_video(chat_id, f, reply_markup=markup)
        os.remove("temp.mp4")
    except:
        bot.send_message(chat_id, "❌ Помилка при відправці відео.")

# === Платіжна кнопка ===
@bot.callback_query_handler(func=lambda c: c.data == "get_premium")
def handle_premium_button(call):
    bot.answer_callback_query(call.id)
    prices = [LabeledPrice(label='Доступ до HD відео', amount=5000)]  # 50 грн = 5000 копійок
    bot.send_invoice(
        chat_id=call.message.chat.id,
        title="Преміум HD доступ",
        description="Дозволяє завантажувати відео в HD/FullHD якості.",
        provider_token=PROVIDER_TOKEN,
        currency="UAH",
        prices=prices,
        start_parameter="premium-hd",
        payload="premium-purchase"
    )

# === Обробка успішного платежу ===
@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    user_id = message.chat.id
    add_premium(user_id)
    bot.send_message(user_id, "✅ Дякуємо за оплату! Тепер ти маєш доступ до HD відео 🎉")

# === Старт бота ===
print("✅ Бот запущено")
bot.remove_webhook()
bot.polling()
