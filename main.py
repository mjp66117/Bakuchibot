import os
import requests
import jdatetime
from time import sleep
from datetime import datetime

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
WEATHER_API = os.getenv("WEATHER_API")

def send_weather():
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q=Baku&appid={WEATHER_API}&units=metric"
        r = requests.get(url).json()

        temp = round(r["main"]["temp"])
        humidity = r["main"]["humidity"]
        wind = round(r["wind"]["speed"] * 3.6)
        desc = r["weather"][0]["description"]

        emoji = "🌤"
        if "rain" in desc:
            emoji = "🌧"
        elif "cloud" in desc:
            emoji = "☁️"
        elif "clear" in desc:
            emoji = "☀️"

        today_shamsi = jdatetime.datetime.now().strftime("%Y/%m/%d")
        today_miladi = datetime.now().strftime("%Y/%m/%d")

        message = f"""
{emoji} باکوچی | وضعیت هوای باکو

📅 شمسی: {today_shamsi}
📆 میلادی: {today_miladi}

🌡 دما: {temp}°C
💨 باد: {wind} km/h
💧 رطوبت: {humidity}%
🌦 وضعیت: {desc}
"""

        send_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        data = {
            "chat_id": CHAT_ID,
            "text": message
        }

        res = requests.post(send_url, data=data)

        print("Telegram response:", res.text)

    except Exception as e:
        print("ERROR:", e)

print("Bot started...")

while True:
    send_weather()
    sleep(60)
