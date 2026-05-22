import os
import requests
import jdatetime
from time import sleep
from datetime import datetime
from telegram import Bot

# =====================
# CONFIG
# =====================
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
WEATHER_API = os.getenv("WEATHER_API")

bot = Bot(token="BOT_TOKEN")

# =====================
# WEATHER TEXT LOGIC
# =====================
def send_weather():
    print("TEST RUN")

    bot.send_message(chat_id=CHAT_ID, text="test message")

    if "rain" in desc:
        return "🌧 امروز بارونیه، چتر یادت نره"
    elif "thunder" in desc or "storm" in desc:
        return "⛈ هوا طوفانیه، بیرون رفتن توصیه نمیشه"
    elif "cloud" in desc:
        return "☁️ آسمون کمی ابریه"
    elif temp >= 30:
        return "🔥 هوا خیلی گرمه، آب زیاد بخور"
    elif temp >= 20:
        return "🌊 هوا عالیه برای بیرون رفتن"
    else:
        return "🧥 هوا خنکه، لباس گرم بپوش"

# =====================
# MAIN FUNCTION
# =====================
def send_weather():
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q=Baku&appid={WEATHER_API}&units=metric&lang=en"
        r = requests.get(url).json()

        # Debug API
        if "main" not in r:
            print("API ERROR:", r)
            return

        temp = round(r["main"]["temp"])
        humidity = r["main"]["humidity"]
        wind = round(r["wind"]["speed"] * 3.6)
        desc = r["weather"][0]["description"]

        # Emoji
        if "rain" in desc:
            emoji = "🌧"
        elif "cloud" in desc:
            emoji = "☁️"
        elif "clear" in desc:
            emoji = "☀️"
        elif "storm" in desc:
            emoji = "⛈"
        else:
            emoji = "🌤"

        # Dates
        today_shamsi = jdatetime.datetime.now().strftime("%Y/%m/%d")
        today_miladi = datetime.now().strftime("%Y/%m/%d")

        # Message
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

        print("Message sent successfully")

    except Exception as e:
        print("ERROR:", e)

# =====================
# START BOT
# =====================
print("Bot started...")

while True:
    send_weather()
    sleep(60)
