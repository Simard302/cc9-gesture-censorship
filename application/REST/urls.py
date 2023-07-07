from django.urls import path, include
from REST.views import fakedata

urlpatterns = [
    path('test', fakedata.fake_data)
]