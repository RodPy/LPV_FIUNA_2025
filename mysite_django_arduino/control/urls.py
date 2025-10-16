from django.urls import path
from .views import panel, do_blink

urlpatterns = [
    path('', panel, name='panel'),
    path('blink/', do_blink, name='blink'),
]
