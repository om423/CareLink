from django.shortcuts import render
from accounts.views import patient_required


@patient_required
def index(request):
    return render(request, "triage/index.html")
