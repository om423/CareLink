from django.shortcuts import render
from accounts.views import doctor_required, patient_required


@doctor_required
def index(request):
    """Doctor dashboard - only accessible to doctors."""
    return render(request, "doctors/index.html")


@patient_required
def find_doctor(request):
    """Find a doctor page - only accessible to patients."""
    return render(request, "doctors/find_doctor.html")
