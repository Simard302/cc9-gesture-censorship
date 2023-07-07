from django.urls import path, include
from REST.views import fakedata

urlpatterns = [
    path('test', fakedata.fake_data),
    path('eric_data', fakedata.my_data),
    path('eric_data/<int:mynum>', fakedata.my_data)
]