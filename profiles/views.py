from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from profiles.forms import ProfileForm
from profiles.models import PatientProfile


def index(request):
    """Redirect to profile edit page."""
    if request.user.is_authenticated:
        return redirect('profiles:edit')
    return redirect('accounts:login')


@login_required
def edit_profile(request):
    """Edit patient profile view."""
    profile, created = PatientProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profiles:edit')
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'profiles/edit_profile.html', {
        'form': form,
        'profile': profile
    })
