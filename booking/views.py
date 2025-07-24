from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from .forms import BookingForm
from .models import Booking

# Bron qilish
def kurs_view(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            # Foydalanuvchi telefon raqamini sessionga yozamiz
            request.session['phone'] = form.cleaned_data['phone']
            return redirect('success')
    else:
        form = BookingForm()
    return render(request, 'booking.html', {'form': form})

# Success – Foydalanuvchining bronlari
def success_view(request):
    phone = request.session.get('phone')
    bookings = []
    if phone:
        bookings = Booking.objects.filter(phone=phone).order_by('-date', '-time')
    return render(request, 'success.html', {'bookings': bookings})

# Admin panel
def panel_view(request):
    bookings = Booking.objects.all().order_by('date', 'time')  # ✅ ketma-ketlik
    bookings_by_date = Booking.objects.values('date').annotate(count=Count('id')).order_by('date')
    return render(request, 'panel.html', {'bookings': bookings, 'bookings_by_date': bookings_by_date})

@csrf_exempt
def cancel_booking_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        reason = request.POST.get('reason', '')
        booking.is_cancelled = True
        booking.cancel_reason = reason
        booking.save()
        return render(request, 'booking/cancel_success.html')

    return render(request, 'booking/cancel_form.html', {'booking': booking})

import json
from django.http import JsonResponse
from .utils import send_telegram
from .models import Booking
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def telegram_webhook(request):
    if request.method == "POST":
        data = json.loads(request.body)
        message = data.get("message", {})
        chat = message.get("chat", {})
        text = message.get("text", "")
        chat_id = chat.get("id")

        if text == "/start":
            send_telegram(chat_id, "Salom! 📲 Iltimos, bron qilgan telefon raqamingizni yuboring. (masalan: +998901234567)")

        elif text.startswith("+998"):
            # 1. Bu chat_id boshqa raqam bilan allaqachon bog‘langanmikan?
            if Booking.objects.filter(chat_id=chat_id).exists():
                old_booking = Booking.objects.filter(chat_id=chat_id).first()
                if old_booking.phone != text:
                    send_telegram(chat_id, "❌ Siz boshqa telefon raqami bilan bog‘langansiz. Avvalgi raqamni bekor qiling.")
                    return JsonResponse({"ok": True})

            # 2. Shu telefon raqam bilan bog‘lanmagan aktiv bronlarni qidiramiz
            bookings = Booking.objects.filter(phone=text, date__gte=now().date(), chat_id__isnull=True, is_cancelled=False)
            if bookings.exists():
                for b in bookings:
                    b.chat_id = chat_id
                    b.save()
                send_telegram(chat_id, "✅ Chat ID muvaffaqiyatli bog‘landi! Endi Telegram eslatmalar olasiz. 😊")
            else:
                send_telegram(chat_id, "❌ Bu raqam bilan aktiv bron topilmadi yoki u allaqachon bog‘langan.")
        
        else:
            send_telegram(chat_id, "🤖 Noma'lum buyruq. Iltimos, telefon raqamingizni yuboring.")

    return JsonResponse({"ok": True})
