from django.urls import path
from . import views

app_name = 'vk_login'
urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout, name='logout'),
]
