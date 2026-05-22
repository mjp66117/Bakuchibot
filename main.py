import os
import requests
import jdatetime

from telegram import Bot
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
WEATHER_API = os.getenv("WEATHER_API")

bot = Bot(token=TOKEN)

def weather_comment(temp, desc):

    desc_lower = desc.lower()

    if "rain" in desc_lower:
        return "🌧 امروز باکو بارونیه، چتر یادت نره"
    
    elif "cloud" in desc_lower:
        return "☁️ آسمون باکو امروز ابری و آرومه"
    
    elif temp >= 30:
        return "🔥 هوای باکو حسابی گرمه، آب زیاد بخور"
    
    elif temp >= 20:
        return "🌊 باکو امروز حال دریاست، وقت ساحله"
    
    else:
        return "🧥 هوا خنکه، لباس مناسب بپوش"

def weather_emoji(desc):

    desc_lower = desc.lower()

    if "clear" in desc_lower:
        return "☀️"

    elif "cloud" in desc_lower:
        return "☁️"

    elif "rain" in desc_lower:
        return "🌧"

    elif "storm" in desc_lower:
        return "⛈"

    elif "snow" in desc_lower:
        return "❄️"

    else:
        return "🌤"

def send_weather():

    url = f"https://api.openweathermap.org/data/2.5/weather?q=Baku&appid={WEATHER_API}&units=metric&lang=en"

    response = requests.get(url).json()

    temp = round(response["main"]["temp"])
    humidity = response["main"]["humidity"]
    wind = round(response["wind"]["speed"] * 3.6)
    desc = response["weather"][0]["description"]

    emoji = weather_emoji(desc)

    comment = weather_comment(temp, desc)

    today_miladi = datetime.now().strftime("%d %B %Y")

    today_shamsi = jdatetime.datetime.now().strftime("%d %B %Y")

    message = f"""
{emoji} باکوچی | وضعیت هوای باکو

📅 شمسی: {today_shamsi}
📆 میلادی: {today_miladi}

🌡 دما: {temp}°C
💨 باد: {wind} km/h
💧 رطوبت: {humidity}%
🌦 وضعیت: {desc}

💬 {comment}

@bakuchi_official_channel
"""

    bot.send_message(chat_id=CHAT_ID, text=message)

scheduler = BlockingScheduler()

scheduler.add_job(send_weather, "cron", hour=9, minute=0)

print("Bot started...")

scheduler.start()
