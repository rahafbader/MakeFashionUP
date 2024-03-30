from django.shortcuts import render, get_object_or_404, redirect 
from django.contrib.auth.decorators import login_required 
from .models import Category, Product, Order, OrderItem 
 
def product_list(request): 
    products = Product.objects.all() 
    return render(request, 'web_project/home.html', {'products': products}) 
 
def product_detail(request, product_id): 
    product = get_object_or_404(Product, pk=product_id) 
    return render(request, 'web_project/product.html', {'product': product}) 
 
@login_required 
def add_to_cart(request, product_id): 
    product = get_object_or_404(Product, pk=product_id) 
    order, created = Order.objects.get_or_create(user=request.user, is_ordered=False) 
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product) 
    order_item.quantity += 1 
    order_item.save() 
    return redirect('product_list') 
 
@login_required 
def view_cart(request): 
    order = Order.objects.get(user=request.user, is_ordered=False) 
    order_items = order.orderitem_set.all() 
    return render(request, 'web_project/view_cart.html', {'order': order, 'order_items': order_items}) 
 
@login_required 
def checkout(request): 
    order = Order.objects.get(user=request.user, is_ordered=False) 
    order.is_ordered = True 
    order.save() 
    return render(request, 'web_project/checkout.html', {'order': order})