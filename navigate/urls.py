from django.urls import path
from .views import navi_view

urlpatterns = [
    path('', navi_view, name='navigate'),
]
