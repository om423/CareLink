from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def index(request):
    """Display triage dashboard."""
    context = {
        'template_data': {'title': 'Triage - CareLink'}
    }
    return render(request, 'triage/index.html', context)

@login_required
def create_triage(request):
    """Create a new triage request."""
    context = {
        'template_data': {'title': 'New Triage Request - CareLink'}
    }
    return render(request, 'triage/create.html', context)

@login_required
def detail(request, pk):
    """View triage detail."""
    context = {
        'template_data': {'title': 'Triage Details - CareLink'},
        'triage_id': pk,
    }
    return render(request, 'triage/detail.html', context)

@login_required
def history(request):
    """View triage history."""
    context = {
        'template_data': {'title': 'Triage History - CareLink'}
    }
    return render(request, 'triage/history.html', context)
