from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path("login/", views.loginUser, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("register/", views.registerUser, name="register"),
    
    path('account/', views.userAccount, name='account'),
    path('edit-account/', views.editAccount, name='edit-account'),
    
    path('delete-skill/<str:id>', views.deleteSkill, name='delete-skill'),
    path('create-skill/', views.createSkill, name='create-skill'),
    path('edit-skill/<str:id>/', views.editSkill, name='edit-skill'),
    
    path('', views.profiles, name='profiles'),
    path('profile/<str:id>/', views.userProfile, name='user-profile'),
    
]
