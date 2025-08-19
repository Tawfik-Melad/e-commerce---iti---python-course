from django.urls import path
from .views import (
    CategoryListView, 
    CategoryDetailView, 
    CategoryCreateView, 
    CategoryUpdateView, 
    CategoryDeleteView
)

# Category URL patterns
urlpatterns = [
    # Category listing
    path('', CategoryListView.as_view(), name='category-list'),
    
    # Category creation
    path('create/', CategoryCreateView.as_view(), name='category-create'),
    
    # Category detail view
    path('<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    
    # Category management
    path('<int:pk>/update/', CategoryUpdateView.as_view(), name='category-update'),
    path('<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),
]