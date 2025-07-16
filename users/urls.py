from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path("login/", views.loginUser, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("register/", views.registerUser, name="register"),
    
    path('', views.profiles, name='profiles'),
    path('profile/<str:id>/', views.userProfile, name='user-profile')
]
