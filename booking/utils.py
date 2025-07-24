import requests

TELEGRAM_BOT_TOKEN = '7972452318:AAGHajPfKiIvvqw_F_jzHKwiRVeybsr8t8s'  # <-- BotFather'dan olingan tokenni shu yerga yoz

def send_telegram(chat_id, message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message
    }
    try:
        response = requests.post(url, data=data)
        return response.json()
    except Exception as e:
        print("❌ Telegram yuborishda xatolik:", e)
        return None
