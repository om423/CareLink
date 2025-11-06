from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import PermissionDenied
from accounts.forms import UserRegistrationForm
from profiles.models import PatientProfile


def index(request):
    """Redirect to login page."""
    if request.user.is_authenticated:
        return redirect('profiles:edit')
    return redirect('accounts:login')


def register_view(request):
    """User registration view."""
    if request.user.is_authenticated:
        return redirect('home:index')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created successfully for {user.username}! Please log in.')
            return redirect('accounts:login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """User login view."""
    if request.user.is_authenticated:
        return redirect('home:index')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next', 'home:index')
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    """User logout view."""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home:index')


def get_user_role(user):
    """Helper function to get user role."""
    try:
        return user.patient_profile.role
    except PatientProfile.DoesNotExist:
        return 'patient'  # Default to patient


def patient_required(view_func):
    """Decorator to ensure user is a patient."""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        role = get_user_role(request.user)
        if role != 'patient':
            messages.error(request, 'Access denied. This page is for patients only.')
            return redirect('home:index')
        return view_func(request, *args, **kwargs)
    return wrapper


def doctor_required(view_func):
    """Decorator to ensure user is a doctor/admin."""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        role = get_user_role(request.user)
        if role != 'doctor':
            messages.error(request, 'Access denied. This page is for doctors/admins only.')
            return redirect('home:index')
        return view_func(request, *args, **kwargs)
    return wrapper
