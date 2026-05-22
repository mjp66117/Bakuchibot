import os
import json
import requests
import jdatetime

from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CITIES_FILE = os.path.join(BASE_DIR, "cities.json")
FACTS_FILE = os.path.join(BASE_DIR, "facts.json")

CITY_INDEX_FILE = os.path.join(BASE_DIR, "city_index.txt")
FACT_INDEX_FILE = os.path.join(BASE_DIR, "fact_index.txt")

IMAGES_DIR = os.path.join(BASE_DIR, "images")

print("BAKUCHI BOT RUNNING")


# ---------------- WEATHER ----------------

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

        send_message(message)

    except Exception as e:
        print("WEATHER ERROR:")
        print(e)


# ---------------- SEND MESSAGE ----------------

def send_message(message):

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    r = requests.post(url, data=data)

    print(r.text)


# ---------------- LOAD JSON ----------------

def load_json(file_path):

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------- GET NEXT ITEM ----------------

def get_next_item(json_file, index_file):

    items = load_json(json_file)

    if not os.path.exists(index_file):

        with open(index_file, "w") as f:
            f.write("0")

    with open(index_file, "r") as f:
        index = int(f.read().strip())

    if index >= len(items):
        return None

    item = items[index]

    with open(index_file, "w") as f:
        f.write(str(index + 1))

    return item


# ---------------- CITY POST ----------------

def send_city():

    try:

        city = get_next_item(CITIES_FILE, CITY_INDEX_FILE)

        if city is None:
            print("ALL CITIES FINISHED")
            return

        caption = city["text"]

        image_path = os.path.join(
            IMAGES_DIR,
            city["image"]
        )

        url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"

        with open(image_path, "rb") as photo:

            files = {
                "photo": photo
            }

            data = {
                "chat_id": CHAT_ID,
                "caption": caption
            }

            r = requests.post(
                url,
                data=data,
                files=files
            )

            print(r.text)

    except Exception as e:
        print("CITY ERROR:")
        print(e)


# ---------------- FACT POST ----------------

def send_fact():

    try:

        fact = get_next_item(
            FACTS_FILE,
            FACT_INDEX_FILE
        )

        if fact is None:
            print("ALL FACTS FINISHED")
            return

        message = f"""
🧠 دانستنی امروز

{fact}

@bakuchi_official_channel
"""

        send_message(message)

    except Exception as e:
        print("FACT ERROR:")
        print(e)


# ---------------- SCHEDULER ----------------

scheduler = BlockingScheduler()

# 9 صبح باکو
scheduler.add_job(
    send_weather,
    "cron",
    hour=5,
    minute=0
)

# 3 عصر باکو
scheduler.add_job(
    send_city,
    "cron",
    hour=11,
    minute=0
)

# 9 شب باکو
scheduler.add_job(
    send_fact,
    "cron",
    hour=17,
    minute=0
)

print("SCHEDULER STARTED")
send_weather()
send_city()
send_fact()
scheduler.start()
