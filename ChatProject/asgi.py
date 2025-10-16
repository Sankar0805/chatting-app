import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from ChatApp import routing  # your app routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ChatProject.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(   # wrap WebSocket routing
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})
