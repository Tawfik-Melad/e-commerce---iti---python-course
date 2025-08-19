"""
URL configuration for marktPlace project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

# Main URL patterns
urlpatterns = [
    # Home page - redirect to products
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False), name='home'),
    
    # Django admin
    path('admin/', admin.site.urls),
    
    # Authentication URLs
    path('accounts/', include('accounts.urls')),
    
    # Core application URLs
    path('products/', include('products.urls')),
    path('category/', include('category.urls')),
    path('cart/', include('cart.urls')),
    
    # Static pages
    path('about/', include('aboutus.urls')),
    path('contact/', include('contactus.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
