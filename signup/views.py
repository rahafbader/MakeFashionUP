from django.contrib.auth.models import User 
from django.shortcuts import render, redirect 
from django.contrib import messages 
from django.contrib.auth import login 
from django.core.exceptions import ValidationError 
def signup(request): 
    if request.method == 'POST': 
        username = request.POST.get('username') 
        email = request.POST.get('email') 
        password = request.POST.get('password') 
        confirm_password = request.POST.get('confirm_password') 
 
        if password != confirm_password: 
            messages.error(request, 'Passwords do not match.') 
            return redirect('signup') 
         
        if User.objects.filter(username=username).exists(): 
            messages.error(request, 'Username is already taken.') 
            return redirect('signup') 
         
        if User.objects.filter(email=email).exists(): 
            messages.error(request, 'Email is already in use.') 
            return redirect('signup') 
         
        try: 
            user = User.objects.create_user(username=username, email=email, password=password) 
            user.save() 
            messages.success(request,"signup successfly") 
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')   
            return redirect('product_list')   
        except ValidationError as e: 
            messages.error(request, 'Error creating user: {}'.format(e)) 
            return redirect('signup') 
    else: 
        return render(request, 'web_project/signup.html')