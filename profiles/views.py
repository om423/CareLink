from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def index(request):
    """Display profiles."""
    context = {
        'template_data': {'title': 'Profiles - CareLink'}
    }
    return render(request, 'profiles/index.html', context)

@login_required
def my_profile(request):
    """Display current user's profile."""
    context = {
        'template_data': {'title': 'My Profile - CareLink'}
    }
    return render(request, 'profiles/my_profile.html', context)

@login_required
def create_profile(request):
    """Create a new profile."""
    context = {
        'template_data': {'title': 'Create Profile - CareLink'}
    }
    return render(request, 'profiles/create_profile.html', context)

@login_required
def edit_profile(request):
    """Edit current user's profile."""
    context = {
        'template_data': {'title': 'Edit Profile - CareLink'}
    }
    return render(request, 'profiles/edit_profile.html', context)
