from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/<str:role>/', views.login, name='login'),
    path('register/<str:role>/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
]
