from django.db import models
from django.shortcuts import render
from django.utils import timezone

from accounts.views import doctor_required, patient_required
from triage.models import TriageInteraction


@doctor_required
def index(request):
    """Doctor dashboard - only accessible to doctors."""
    # Calculate stats from actual database
    total_reports = TriageInteraction.objects.count()
    today = timezone.now().date()
    today_reports = TriageInteraction.objects.filter(created_at__date=today).count()

    # Count high-risk patients (Critical or Severe severity)
    high_risk_count = TriageInteraction.objects.filter(severity__in=["Critical", "Severe"]).count()

    # Count unique active patients
    active_patients = TriageInteraction.objects.values("user").distinct().count()

    # Get recent triage reports ordered by severity and time
    severity_order = models.Case(
        models.When(severity="Critical", then=4),
        models.When(severity="Severe", then=3),
        models.When(severity="Moderate", then=2),
        models.When(severity="Mild", then=1),
        default=0,
        output_field=models.IntegerField(),
    )

    recent_reports = (
        TriageInteraction.objects.select_related("user")
        .annotate(severity_rank=severity_order)
        .order_by("-severity_rank", "-updated_at")[:10]
    )

    # Calculate today's summary stats
    reports_reviewed_today = 0  # Placeholder
    appointments_today = 0  # Placeholder
    follow_ups_required = TriageInteraction.objects.filter(
        severity__in=["Critical", "Severe"]
    ).count()

    context = {
        "total_reports": total_reports,
        "today_reports": today_reports,
        "high_risk_count": high_risk_count,
        "active_patients": active_patients,
        "recent_reports": recent_reports,
        "reports_reviewed_today": reports_reviewed_today,
        "appointments_today": appointments_today,
        "follow_ups_required": follow_ups_required,
    }
    return render(request, "doctors/index.html", context)


@patient_required
def find_doctor(request):
    """Find a doctor page - only accessible to patients."""
    return render(request, "doctors/find_doctor.html")
