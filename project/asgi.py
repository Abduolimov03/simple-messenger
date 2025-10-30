import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

import users.routing
import messages.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telegram_backend.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),

    "websocket": AuthMiddlewareStack(
        URLRouter(
            users.routing.websocket_urlpatterns +
            messages.routing.websocket_urlpatterns
        )
    ),
})
