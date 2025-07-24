from django.core.management.base import BaseCommand
from booking.models import Booking
from datetime import datetime, timedelta
from booking.utils import send_telegram

class Command(BaseCommand):
    help = 'Bugungi va ertangi bronlarga Telegram orqali eslatma yuboradi'

    def handle(self, *args, **kwargs):
        now = datetime.now()
        today = now.date()
        two_hours_later = now + timedelta(hours=2)

        # 🕑 Bugungi — 2 soat ichidagi bronlar
        bookings_today = Booking.objects.filter(
            date=today,
            time__gte=now.time(),
            time__lte=two_hours_later.time(),
            is_cancelled=False,
            chat_id__isnull=False
        ).distinct()

        # 📅 Ertangi bronlar
        tomorrow = today + timedelta(days=1)
        bookings_tomorrow = Booking.objects.filter(
            date=tomorrow,
            is_cancelled=False,
            chat_id__isnull=False
        ).distinct()

        count = 0

        for booking in bookings_today.union(bookings_tomorrow):
            # ❗ Faqat agar bu chat_id shu phone raqam bilan avval bog‘langan bo‘lsa
            if Booking.objects.filter(phone=booking.phone, chat_id=booking.chat_id).exists():
                if booking.date == today:
                    msg = f"📅 Bugun soat {booking.time.strftime('%H:%M')} da soch oldirishga bron qilgansiz. Sizni kutamiz, {booking.name}! 💈"
                else:
                    msg = f"📅 Ertaga soat {booking.time.strftime('%H:%M')} da soch oldirishga kelishingizni unutmang, {booking.name}! 💈"
                send_telegram(booking.chat_id, msg)
                count += 1

        self.stdout.write(self.style.SUCCESS(f"✅ {count} ta Telegram eslatma yuborildi."))
