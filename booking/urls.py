from django.urls import path
from . import views

urlpatterns = [
    path('booking/', views.kurs_view, name='booking'),
    path('booking/success/', views.success_view, name='success'),
    path('panel/', views.panel_view, name='panel'),
    path('booking/cancel/<int:booking_id>/', views.cancel_booking_view, name='cancel_booking'),

    # 👉 Telegram webhook uchun yo‘l
    path('telegram-webhook/', views.telegram_webhook, name='telegram_webhook'),
]

