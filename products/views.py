from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Product
from .forms import ProductForm
from category.models import Category

def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'products/product_list.html', {'products': products})

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            # 1. Save product object (without committing categories yet)
            product = form.save(commit=False)
            product.owner = request.user  # Set the owner
            product.save()

            # 2. Handle categories input
            categories_input = form.cleaned_data.get("categories_input", "")
            if categories_input:
                names = [c.strip() for c in categories_input.split(",") if c.strip()]
                for name in names:
                    category, created = Category.objects.get_or_create(name=name)
                    product.categories.add(category)

            messages.success(request, 'Product created successfully!')
            return redirect('product_list')
    else:
        form = ProductForm()

    return render(request, 'products/product_form.html', {'form': form, 'title': 'Create Product'})

@login_required
def product_update(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Check if user owns this product
    if product.owner != request.user:
        messages.error(request, 'You do not have permission to edit this product.')
        return redirect('product_detail', product_id=product.id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            # 1. Save product object (without committing categories yet)
            product = form.save(commit=False)
            product.save()

            # 2. Clear existing categories and add new ones
            product.categories.clear()
            categories_input = form.cleaned_data.get("categories_input", "")
            if categories_input:
                names = [c.strip() for c in categories_input.split(",") if c.strip()]
                for name in names:
                    category, created = Category.objects.get_or_create(name=name)
                    product.categories.add(category)

            messages.success(request, 'Product updated successfully!')
            return redirect('product_detail', product_id=product.id)
    else:
        # Pre-populate categories input with existing categories
        existing_categories = ", ".join([cat.name for cat in product.categories.all()])
        form = ProductForm(instance=product, initial={'categories_input': existing_categories})

    return render(request, 'products/product_form.html', {'form': form, 'title': 'Update Product'})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/product_detail.html', {'product': product})

@login_required
def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Check if user owns this product
    if product.owner != request.user:
        messages.error(request, 'You do not have permission to delete this product.')
        return redirect('product_detail', product_id=product.id)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('product_list')
    
    return render(request, 'products/product_delete.html', {'product': product})