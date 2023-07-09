from django.urls import path, include
from streamapp import views

urlpatterns = [
    path('', include('Frontend.urls')),
    path('api/', include('REST.urls')),
    path('streaming/', views.stream_view, name='stream'),
]