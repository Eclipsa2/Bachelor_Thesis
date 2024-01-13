from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register_user, name="register"),
    path('chat/<int:chat_session_id>/', views.chat_session_detail, name='chat_session_detail'),
]
