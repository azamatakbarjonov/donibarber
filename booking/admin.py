from django.contrib import admin, messages
from .models import Booking
from datetime import datetime, timedelta
from .utils import send_telegram

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'date', 'time', 'is_cancelled')
    actions = ['send_telegram_reminders']

    def send_telegram_reminders(self, request, queryset):
        now = datetime.now()
        today = now.date()
        two_hours_later = now + timedelta(hours=2)

        count = 0

        # Bugungi bronlar (2 soat qolgani)
        bookings_today = Booking.objects.filter(
            date=today,
            time__gte=now.time(),
            time__lte=two_hours_later.time(),
            is_cancelled=False
        )
        for booking in bookings_today:
            if booking.chat_id:
                msg = f"📅 Bugun soat {booking.time.strftime('%H:%M')} da soch oldirishga bron qilgansiz. Sizni kutamiz, {booking.name}! 💈"
                send_telegram(booking.chat_id, msg)
                count += 1

        # Ertangi bronlar
        tomorrow = today + timedelta(days=1)
        bookings_tomorrow = Booking.objects.filter(date=tomorrow, is_cancelled=False)
        for booking in bookings_tomorrow:
            if booking.chat_id:
                msg = f"📅 Ertaga soat {booking.time.strftime('%H:%M')} da soch oldirishga kelishingizni unutmang, {booking.name}! 💈"
                send_telegram(booking.chat_id, msg)
                count += 1

        self.message_user(request, f"✅ {count} ta Telegram eslatma yuborildi.", level=messages.SUCCESS)

    send_telegram_reminders.short_description = "📨 Telegram eslatmalarni yuborish"
