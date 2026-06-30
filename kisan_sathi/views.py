from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'login.html')

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if password != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'signup.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'signup.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return render(request, 'signup.html')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        
        login(request, user)
        messages.success(request, 'Account created successfully!')
        return redirect('dashboard')
    
    return render(request, 'signup.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('home')

@login_required(login_url='login')
def dashboard_view(request):
    return render(request, 'dashboard/code.html')
@login_required(login_url='login')
def disease_detector_view(request):
    return render(request, 'disease_detector/code.html')

@login_required(login_url='login')
def weather_view(request):
    return render(request, 'weather/code.html')

@login_required(login_url='login')
def chatbot_view(request):
    return render(request, 'chatbot/code.html')
