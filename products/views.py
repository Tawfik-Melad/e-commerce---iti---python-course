from django.shortcuts import render
from django.http import HttpResponse
from models import Product
from django.shortcuts import get_object_or_404 , redirect
# Create your views here.

def products(request):
    return render(request, 'index.html')

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/products.html', {'products': products})


def create_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        instock_items = request.POST.get('instock_items')
        description = request.POST.get('description')

        product = Product(
            name=name,
            price=price,
            image=image,
            instock_items=instock_items,
            description=description
        )
        product.save()
        return HttpResponse("Product created successfully!")
    
    return render(request, 'products/create_product.html')  # Render form for creating a product

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product is None:
        return render(request, 'page404.html', status=404)
    
    return render(request, 'products/product_detail.html', {'product': product})

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        return HttpResponse("Product deleted successfully!")
    
    return redirect('product_list')  # Redirect to product list after deletion