import os
from time import sleep

print("START FILE")

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
WEATHER_API = os.getenv("WEATHER_API")

print("BOT_TOKEN:", TOKEN)
print("CHAT_ID:", CHAT_ID)
print("API:", WEATHER_API)

def send_weather():
    print("SEND WEATHER CALLED")

print("Bot started...")

i = 0
while True:
    i += 1
    print("LOOP RUN:", i)
    send_weather()
    sleep(10)
