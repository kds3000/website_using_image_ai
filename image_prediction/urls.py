from django.urls import path
from . import views

app_name = 'image_prediction'
urlpatterns = [
    path('', views.index, name='index'),
    ]

