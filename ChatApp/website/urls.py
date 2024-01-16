from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register_user, name="register"),
    path('chat/<int:chat_session_id>/', views.chat_session_detail, name='chat_session_detail'),
    path('start_new_chat/', views.start_new_chat, name='start_new_chat'),
    path('delete_chat/<int:chat_session_id>/', views.delete_chat, name='delete_chat'),
]
