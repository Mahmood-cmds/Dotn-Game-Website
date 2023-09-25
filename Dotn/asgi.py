# asgi.py

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from dotn_game.routing import websocket_urlpatterns
from channels.auth import AuthMiddlewareStack
import django 
from channels.routing import get_default_application 

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
