from django.urls import path
from . import views

app_name = 'object_detection'
urlpatterns = [
    path('', views.index, name='index'),
]

