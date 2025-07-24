from django.urls import path
from .views import price_view

urlpatterns = [
    path('', price_view, name='price'),
]
