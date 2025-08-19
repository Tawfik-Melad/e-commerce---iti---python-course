from django.urls import path
from . import views

# Product URL patterns
urlpatterns = [
    # Product listing
    path('', views.product_list, name='product_list'),
    
    # Product creation (requires login)
    path('create/', views.product_create, name='product_create'),
    
    # Product detail view
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    
    # Product management (requires login + ownership)
    path('<int:product_id>/update/', views.product_update, name='product_update'),
    path('<int:product_id>/delete/', views.product_delete, name='product_delete'),
]