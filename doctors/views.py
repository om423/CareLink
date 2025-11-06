from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def index(request):
    """Display doctors directory."""
    context = {
        'template_data': {'title': 'Find a Doctor - CareLink'}
    }
    return render(request, 'doctors/index.html', context)

@login_required
def dashboard(request):
    """Doctor dashboard."""
    context = {
        'template_data': {'title': 'Doctor Dashboard - CareLink'}
    }
    return render(request, 'doctors/dashboard.html', context)

@login_required
def triage_reports(request):
    """View triage reports."""
    context = {
        'template_data': {'title': 'Triage Reports - CareLink'}
    }
    return render(request, 'doctors/triage_reports.html', context)

@login_required
def clinic_info(request):
    """Manage clinic information."""
    context = {
        'template_data': {'title': 'Clinic Information - CareLink'}
    }
    return render(request, 'doctors/clinic_info.html', context)
