import os
import requests
import jdatetime
from time import sleep
from datetime import datetime
from telegram import Bot

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
WEATHER_API = os.getenv("WEATHER_API")

bot = Bot(token=TOKEN)

def weather_comment(temp, desc):
    desc = desc.lower()

    if "rain" in desc:
        return "🌧 امروز بارونیه، چتر یادت نره"
    elif "cloud" in desc:
        return "☁️ آسمون کمی ابریه"
    elif temp >= 30:
        return "🔥 هوا خیلی گرمه"
    elif temp >= 20:
        return "🌊 هوا عالیه برای بیرون رفتن"
    else:
        return "🧥 هوا خنکه"

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

💬 {weather_comment(temp, desc)}

@bakuchi_official_channel
"""

        bot.send_message(chat_id=CHAT_ID, text=message)
        print("MESSAGE SENT")

    except Exception as e:
        print("ERROR:", e)

print("Bot started...")

while True:
    send_weather()
    sleep(60)
