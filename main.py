import os
import requests
import jdatetime

from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

print("BAKUCHI WEATHER BOT RUNNING")

def send_weather():

    try:

        weather_data = requests.get(
            "https://wttr.in/Baku?format=j1"
        ).json()

        current = weather_data["current_condition"][0]

        temp = current["temp_C"]
        humidity = current["humidity"]
        wind = current["windspeedKmph"]
        desc = current["weatherDesc"][0]["value"]

        emoji = "🌤"

        if "rain" in desc.lower():
            emoji = "🌧"
        elif "cloud" in desc.lower():
            emoji = "☁️"
        elif "sun" in desc.lower():
            emoji = "☀️"

        today_shamsi = jdatetime.datetime.now().strftime("%d %B %Y")
        today_miladi = datetime.now().strftime("%d %B %Y")

        message = f"""
{emoji} باکوچی | وضعیت هوای باکو

📅 شمسی: {today_shamsi}
📆 میلادی: {today_miladi}

🌡 دما: {temp}°C
💨 باد: {wind} km/h
💧 رطوبت: {humidity}%
🌦 وضعیت: {desc}

💬 باکو امروز یه حال و هوای خاص داره 😄

@bakuchi_official_channel
"""

        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

        data = {
            "chat_id": CHAT_ID,
            "text": message
        }

        r = requests.post(url, data=data)

        print("TELEGRAM RESPONSE:")
        print(r.text)

    except Exception as e:
        print("ERROR:")
        print(e)

scheduler = BlockingScheduler()

# ساعت 9 صبح باکو (UTC+4)
scheduler.add_job(send_weather, "cron", hour=5, minute=0)

print("SCHEDULER STARTED")

scheduler.start()
