from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Category
from .forms import CategoryForm

# Create your views here.


class CategoryListView(ListView):
    model = Category
    template_name = 'category/category_list.html'
    context_object_name = 'categories'
    ordering = ['name']

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category/category_detail.html'
    context_object_name = 'category'

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/category_form.html'
    success_url = reverse_lazy('category-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Category created successfully!')
        return super().form_valid(form)

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/category_form.html'
    success_url = reverse_lazy('category-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Category updated successfully!')
        return super().form_valid(form)

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'category/category_confirm_delete.html'
    success_url = reverse_lazy('category-list')
    
    def delete(self, request, *args, **kwargs):
        category = self.get_object()
        # Check if category has products
        if category.products.exists():
            messages.error(request, f'Cannot delete category "{category.name}" because it contains products. Please remove or reassign the products first.')
            return redirect('category-detail', pk=category.pk)
        
        messages.success(request, 'Category deleted successfully!')
        return super().delete(request, *args, **kwargs)


