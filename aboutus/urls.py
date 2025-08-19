from django.urls import path
from . import views

# About us URL patterns
urlpatterns = [
    # About us page
    path('', views.about_us, name='about_us'),
]