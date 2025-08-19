from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction
from .models import Cart, CartItem, Order, OrderItem
from .forms import CheckoutForm, CartItemUpdateForm
from products.models import Product

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/cart.html', {'cart': cart})

@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Check if product is already in cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': 1}
        )
        
        if not created:
            # Product already in cart, increase quantity
            cart_item.quantity += 1
            cart_item.save()
        
        messages.success(request, f'{product.name} added to cart!')
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f'{product.name} added to cart!',
                'cart_count': cart.total_items
            })
        
        return redirect('cart_view')
    
    return redirect('product_detail', product_id=product_id)

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    
    messages.success(request, f'{product_name} removed from cart!')
    return redirect('cart_view')

@login_required
def update_cart_item(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        form = CartItemUpdateForm(request.POST, instance=cart_item)
        
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            
            # Check if product has enough stock
            if quantity > cart_item.product.instock_items:
                messages.error(request, f'Only {cart_item.product.instock_items} items available in stock!')
                return redirect('cart_view')
            
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated successfully!')
        
    return redirect('cart_view')

@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    if not cart.items.exists():
        messages.error(request, 'Your cart is empty!')
        return redirect('cart_view')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Create order
                order = form.save(commit=False)
                order.user = request.user
                order.total_amount = cart.total_price
                order.save()
                
                # Create order items
                for cart_item in cart.items.all():
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        quantity=cart_item.quantity,
                        price=cart_item.product.price
                    )
                    
                    # Update product stock
                    cart_item.product.instock_items -= cart_item.quantity
                    cart_item.product.save()
                
                # Clear cart
                cart.items.all().delete()
                
                messages.success(request, f'Order placed successfully! Order number: {order.order_number}')
                return redirect('order_detail', order_id=order.id)
    else:
        form = CheckoutForm()
    
    return render(request, 'cart/checkout.html', {
        'cart': cart,
        'form': form
    })

@login_required
def order_list(request):
    orders = request.user.orders.all().order_by('-created_at')
    return render(request, 'cart/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'cart/order_detail.html', {'order': order}) 