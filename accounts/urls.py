from django.urls import path
from . import views

# Authentication URL patterns
urlpatterns = [
    # User registration and login
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # User profile and management
    path('profile/', views.profile, name='profile'),
    path('my-products/', views.my_products, name='my_products'),
] 