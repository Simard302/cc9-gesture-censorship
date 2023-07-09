# import os
# import django
# from django.core.asgi import get_asgi_application
# from django.urls import path, re_path
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# import django_eventstream

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

# application = ProtocolTypeRouter({
#     'http': URLRouter([
#         path('events/', AuthMiddlewareStack(
#             URLRouter(django_eventstream.routing.urlpatterns)
#         ), { 'channels': ['test'] }),
#         re_path(r'', get_asgi_application()),
#     ]),
# })
import os

from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    # Just HTTP for now. (We can add other protocols later.)
})