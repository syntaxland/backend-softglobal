"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

# core/asgi.py
import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from live_chat.routing import websocket_urlpatterns as live_chat_websocket_urlpatterns

# Define the ASGI application
application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            live_chat_websocket_urlpatterns 
        )
    ),
})
