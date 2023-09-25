
from django.urls import path
from .consumers import RoomConsumer
from django.urls import re_path
websocket_urlpatterns = [
    path('ws/room/<str:room_id>/', RoomConsumer.as_asgi()),
]

