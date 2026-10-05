import urllib.request
import json
import time

TOKEN = "8672778966:AAFBmFpHLtWVudBKoNSg6u8t6fNlbyT15-g"
BASE_URL = f"https://teleapi.ru{TOKEN}/"

def send_message(chat_id, text):
    try:
        data = json.dumps({"chat_id": chat_id, "text": text}).encode("utf-8")
        req = urllib.request.Request(BASE_URL + "sendMessage", data=data)
        req.add_header("Content-Type", "application/json")
        req.add_header("User-Agent", "Mozilla/5.0")
        urllib.request.urlopen(req)
    except Exception:
        pass

def get_updates(offset=None):
    try:
        url = BASE_URL + "getUpdates?timeout=10"
        if offset:
            url += f"&offset={offset}"
        req = urllib.request.Request(url)
        req.add_header("User-Agent", "Mozilla/5.0")
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception:
        return None

print("Бот NextGen_NFT запущен через прокси!")
offset = None

while True:
    updates = get_updates(offset)
    if updates and "result" in updates:
        for update in updates["result"]:
            offset = update["update_id"] + 1
            if "message" in update and "text" in update["message"]:
                chat_id = update["message"]["chat"]["id"]
                user_text = update["message"]["text"]
                if user_text == "/start":
                    send_message(chat_id, "Привет! Бот NextGen_NFT успешно работает прямо с телефона! 🚀")
                else:
                    send_message(chat_id, f"Вы написали: {user_text}")
    time.sleep(2)
