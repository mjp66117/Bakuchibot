import os
import requests
from time import sleep

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

print("BOT IS RUNNING")

def send_test():

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": "✅ بات باکوچی آنلاین شد"
    }

    r = requests.post(url, data=data)

    print(r.text)

while True:
    send_test()
    sleep(60)
