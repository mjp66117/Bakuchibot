import os
import random
import jdatetime
from time import sleep
from datetime import datetime

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def fake_weather():
    weather_list = [
        ("☀️", "آفتابی", "هوا عالیه برای بیرون رفتن 🌊"),
        ("☁️", "ابری", "آسمون کمی گرفته‌ست"),
        ("🌧", "بارونی", "چتر یادت نره 🌂"),
        ("🌤", "نیمه ابری", "هوا متعادل و خوبه")
    ]

    return random.choice(weather_list)

def send_weather():
    emoji, desc, comment = fake_weather()

    today_shamsi = jdatetime.datetime.now().strftime("%Y/%m/%d")
    today_miladi = datetime.now().strftime("%Y/%m/%d")

    message = f"""
{emoji} باکوچی | وضعیت هوای باکو

📅 شمسی: {today_shamsi}
📆 میلادی: {today_miladi}

🌦 وضعیت: {desc}

💬 {comment}
"""

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    res = requests.post(url, data=data)
    print("Telegram response:", res.text)

print("Bot started...")

while True:
    send_weather()
    sleep(60)
