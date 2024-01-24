import os
from django.urls import path
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import chatapp.routing
from chatapp.consumers import ChatConsumer 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chatapp.routing.websocket_urlpatterns
        )
    ),
})

# chatapp/routing.py
websocket_urlpatterns = [
    path('ws/<str:room_name>/', ChatConsumer.as_asgi()),
]

