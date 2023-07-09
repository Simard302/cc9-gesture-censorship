from django.urls import path, include

urlpatterns = [
    path('', include('Frontend.urls')),
    path('api/', include('REST.urls')),
    path('apiStream/', include('STREAM.urls'))
]