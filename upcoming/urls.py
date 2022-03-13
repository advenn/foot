from django.urls import path, include
from .views import *
urlpatterns = [
    path('', main, name='main'),
    path('predict/', predict_receive, name='predict_receive'),
]