import os
import django
import time
import requests
import json

# Django sozlash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from booking.models import Booking
from booking.utils import send_telegram  # send_telegram(chat_id, message)

BOT_TOKEN = '7972452318:AAGHajPfKiIvvqw_F_jzHKwiRVeybsr8t8s'  # <-- o'zgartir
BASE_URL = f'https://api.telegram.org/bot{BOT_TOKEN}'

last_update_id = 0

def get_updates():
    global last_update_id
    url = f'{BASE_URL}/getUpdates?offset={last_update_id + 1}'
    response = requests.get(url)
    result = response.json().get('result', [])
    return result

def handle_message(message):
    chat_id = message['chat']['id']
    text = message.get('text', '')

    if text == '/start':
        send_telegram(chat_id, "Salom! 📲 Iltimos, bron qilgan telefon raqamingizni yuboring. (masalan: +998901234567)")

    elif text.startswith("+998"):
        # 1. Shu raqamli bronlar borligini tekshiramiz
        bookings = Booking.objects.filter(phone=text, is_cancelled=False)

        # 2. Shu chat_id boshqa raqamga ulanganmi — tekshirish
        already_linked = Booking.objects.filter(chat_id=chat_id).exclude(phone=text).exists()

        if already_linked:
            send_telegram(chat_id, "❌ Siz boshqa telefon raqami bilan bog‘langansiz. Avvalgi raqamni bekor qiling.")
            return

        if bookings.exists():
            # 3. Chat ID bog‘laymiz
            for b in bookings:
                b.chat_id = str(chat_id)
                b.save()
            send_telegram(chat_id, "✅ Chat ID muvaffaqiyatli bog‘landi! Endi Telegram eslatmalar olasiz. 😊")
        else:
            send_telegram(chat_id, "❌ Bu raqam bilan aktiv bron topilmadi.")
    else:
        send_telegram(chat_id, "🤖 Noma'lum buyruq. /start yoki telefon raqamingizni yuboring.")

def run_bot():
    global last_update_id
    print("🤖 Bot ishga tushdi. Kutmoqda...")
    while True:
        updates = get_updates()
        for update in updates:
            last_update_id = update['update_id']
            if 'message' in update:
                handle_message(update['message'])
        time.sleep(2)

if __name__ == '__main__':
    run_bot()
