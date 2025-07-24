from django import forms
from .models import Booking
from django.utils import timezone
from django.forms.widgets import DateInput, Select, NumberInput
from datetime import datetime, timedelta
import re

def get_time_choices():
    times = []
    start_time = datetime.strptime("09:00", "%H:%M")
    end_time = datetime.strptime("18:00", "%H:%M")
    while start_time <= end_time:
        times.append((start_time.strftime("%H:%M"), start_time.strftime("%H:%M")))
        start_time += timedelta(minutes=30)
    return times

class BookingForm(forms.ModelForm):
    time = forms.ChoiceField(choices=get_time_choices(), widget=Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Booking
        fields = ['name', 'phone', 'date', 'time', 'people']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+998901234567'}),
            'date': DateInput(attrs={'type': 'text', 'id': 'datepicker', 'class': 'form-control'}),
            'people': NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        pattern = r'^\+998(90|91|93|94|95|97|98|99|33|88)\d{7}$'

        if not re.match(pattern, phone):
            raise forms.ValidationError("📵 Telefon raqam noto‘g‘ri. Masalan: +998901234567")

        return phone

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        people = cleaned_data.get('people')

        if date and time and people:
            # Aware datetime: tanlangan sana + vaqt
            selected_start = timezone.make_aware(
                datetime.combine(date, datetime.strptime(time, "%H:%M").time())
            )
            selected_end = selected_start + timedelta(minutes=30 * people)

            now = timezone.now()

            # ⛔ O‘tgan vaqtga bron qilishni bloklash
            if selected_start < now:
                raise forms.ValidationError("❗ O‘tgan vaqtga bron qilish mumkin emas.")

            # ⛔ Band vaqtni tekshirish
            bookings = Booking.objects.filter(date=date)
            for booking in bookings:
                existing_start = timezone.make_aware(
                    datetime.combine(booking.date, booking.time)
                )
                existing_end = existing_start + timedelta(minutes=30 * booking.people)

                if selected_start < existing_end and existing_start < selected_end:
                    raise forms.ValidationError("❌ Bu vaqt oralig‘i allaqachon band. Iltimos boshqa vaqt tanlang.")

        return cleaned_data

