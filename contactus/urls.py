from django.urls import path
from . import views

# Contact us URL patterns
urlpatterns = [
    # Contact us page
    path('', views.contact_us, name='contact_us'),
]