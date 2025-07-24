# booking/models.py
from django.db import models

class Booking(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    date = models.DateField()
    people = models.PositiveIntegerField(default=1)
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_cancelled = models.BooleanField(default=False)
    cancel_reason = models.TextField(blank=True, null=True)

    chat_id = models.CharField(max_length=50, null=True, blank=True)  # ✅ Telegram uchun

    def __str__(self):
        return f"{self.name} - {self.date} {self.time}"
