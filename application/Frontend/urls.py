from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from Frontend.views import nav

urlpatterns = [
    path("index", nav.index)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)