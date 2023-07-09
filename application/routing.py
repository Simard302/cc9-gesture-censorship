from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path
from streamapp.consumers import StreamConsumer

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter([
        path('stream/', StreamConsumer.as_asgi()),
    ]),
})
