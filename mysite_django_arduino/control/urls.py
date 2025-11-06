from django.urls import path
from .views import panel, do_blink, read_sensor_view

urlpatterns = [
    path('', panel, name='panel'),
    path('blink/', do_blink, name='blink'),
    path('read/<slug:sensor>/', read_sensor_view, name='read_sensor'),

]
