from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('offline/', views.offline_mode, name='offline_mode'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.login_view, name='logout'),
    path('online/', views.online_mode, name='online_mode'),
    path('create_room/', views.create_room, name='create_room'),
    path('enter_room/', views.enter_room, name='enter_room'),
    path('play_online/<str:room_id>/', views.play_online, name='play_online'),
]   
