from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem, Booking
from .forms import BookingForm
from django.contrib import messages


def product_list(request):
    category_name = request.GET.get('category', None)
    if category_name:
        products = Product.objects.filter(category__name__iexact=category_name)
    else:
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
    if created:
        order_item.quantity = 1  
    else:
        order_item.quantity += 1  
    order_item.save()

    total_price = 0
    for item in order.orderitem_set.all():
        total_price += item.product.price * item.quantity
    order.total_price = total_price
    order.save()

    if request.method == 'POST':
        form = BookingForm(request.POST)
        form.instance.service_provider = product.owner
        form.instance.product = product
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.service_provider = product.owner
            booking.product = product
            booking.save()
            return redirect('product_list')
    else:
        form = BookingForm()
    
    return render(request, 'web_project/add_to_cart.html', {'form': form, 'product': product})


@login_required 
def view_cart(request): 
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'web_project/cart.html', {'bookings': bookings})
 
@login_required 
def checkout(request): 
    order = Order.objects.get(user=request.user, is_ordered=False) 
    order.is_ordered = True 
    order.save() 
    return render(request, 'web_project/checkout.html', {'order': order})



@login_required
def update_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)

    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, 'Booking was updated successfully!')
            return redirect('view_cart')
    else:
        form = BookingForm(instance=booking)
    
    return render(request, 'web_project/update_booking.html', {'form': form, 'booking': booking})

@login_required
def delete_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        booking.delete()
        return redirect('view_cart')
    
    return render(request, 'web_project/delete_booking.html', {'booking': booking})