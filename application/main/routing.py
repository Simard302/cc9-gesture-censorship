# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.urls import path
# from streamapp.consumers import StreamConsumer

# application = ProtocolTypeRouter({
#     'http': get_asgi_application(),
#     'websocket': URLRouter([
#         path('stream/', StreamConsumer.as_asgi()),
#     ]),
# })
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/some_url/', consumers.SomeConsumer.as_asgi()),
    # Add more paths for your consumers as needed
]