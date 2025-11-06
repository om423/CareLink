from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def index(request):
    """Account settings page."""
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    context = {
        'template_data': {'title': 'Account Settings - CareLink'}
    }
    return render(request, 'accounts/index.html', context)

def login_view(request):
    """Login view."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Welcome back!')
            return redirect('home:index')
        else:
            messages.error(request, 'Invalid username or password.')
    
    context = {
        'template_data': {'title': 'Login - CareLink'}
    }
    return render(request, 'accounts/login.html', context)

def register_view(request):
    """Registration view."""
    if request.user.is_authenticated:
        messages.info(request, 'You already have an account.')
        return redirect('home:index')
    
    context = {
        'template_data': {'title': 'Register - CareLink'}
    }
    return render(request, 'accounts/register.html', context)

def logout_view(request):
    """Logout view."""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home:index')
