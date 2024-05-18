from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators  import login_required
from home.models import Product, Order, Booking

@login_required
def dashboard(request):
    user = request.user
    products = Product.objects.filter(owner=user)
    orders = Order.objects.filter(user=user)
    bookings = Booking.objects.filter(service_provider=user)  

    context = {
        'products': products,
        'orders': orders,
        'bookings': bookings,
    }
    return render(request, 'web_project/dashboard.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            if Product.objects.filter(owner=user).exists():
                return redirect('dashboard')  
            else:
                return redirect('product_list')  
        else:
            messages.error(request, 'Invalid name or password.')

    return render(request, 'web_project/login.html')


