from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def index(request):
    """Display appointments."""
    context = {
        'template_data': {'title': 'Appointments - CareLink'}
    }
    return render(request, 'appointments/index.html', context)

@login_required
def book_appointment(request):
    """Book a new appointment."""
    context = {
        'template_data': {'title': 'Book Appointment - CareLink'}
    }
    return render(request, 'appointments/book.html', context)

@login_required
def detail(request, pk):
    """View appointment detail."""
    context = {
        'template_data': {'title': 'Appointment Details - CareLink'},
        'appointment_id': pk,
    }
    return render(request, 'appointments/detail.html', context)

@login_required
def my_appointments(request):
    """View user's appointments."""
    context = {
        'template_data': {'title': 'My Appointments - CareLink'}
    }
    return render(request, 'appointments/my_appointments.html', context)
