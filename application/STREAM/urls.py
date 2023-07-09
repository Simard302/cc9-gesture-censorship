from django.urls import path, include
from STREAM.views import ctrl

urlpatterns = [

    path('about',ctrl.about),
    path('contact',ctrl.contact),
    path('index',ctrl.index),
    path('upload',ctrl.upload),
    path('stream',ctrl.stream),
]