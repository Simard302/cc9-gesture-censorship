from django.urls import path, include
from REST.views import fakedata, RestCtrl

urlpatterns = [
    # path('test', fakedata.fake_data),
    # path('eric_data', fakedata.my_data),
    # path('eric_data/<int:mynum>', fakedata.my_data),

    ### 
    path('about',RestCtrl.about),
    path('contact',RestCtrl.contact),
    path('index',RestCtrl.index),
    path('upload',RestCtrl.upload),
]