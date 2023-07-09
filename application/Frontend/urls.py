from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from Frontend.views import nav

urlpatterns = [
    path("about", nav.about),
    path("contact", nav.contact),
    path("index", nav.index),
    path("stream", nav.streamPage),
    path("upload", nav.uploadPage),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)