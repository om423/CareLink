from django.db import models
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
except ImportError:
    letter = None
    canvas = None

from accounts.views import doctor_required, patient_required
from triage.models import TriageDoctorNote, TriageInteraction


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

    # Get unassigned cases (priority queue)
    priority_queue = (
        TriageInteraction.objects.filter(assigned_doctor__isnull=True)
        .select_related("user")
        .annotate(severity_rank=severity_order)
        .order_by("-severity_rank", "-updated_at")
    )

    # Get team cases (assigned to any doctor)
    team_cases = (
        TriageInteraction.objects.filter(assigned_doctor__isnull=False)
        .select_related("user", "assigned_doctor")
        .prefetch_related("notes")
        .annotate(severity_rank=severity_order)
        .order_by("-severity_rank", "-updated_at")
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
        "priority_queue": priority_queue,
        "team_cases": team_cases,
        "reports_reviewed_today": reports_reviewed_today,
        "appointments_today": appointments_today,
        "follow_ups_required": follow_ups_required,
    }
    return render(request, "doctors/index.html", context)


@patient_required
def find_doctor(request):
    """Find a doctor page - only accessible to patients."""
    return render(request, "doctors/find_doctor.html")


@doctor_required
@require_POST
def assign_to_self(request, interaction_id):
    """Assign a triage interaction to the current doctor."""
    interaction = get_object_or_404(TriageInteraction, id=interaction_id)
    interaction.assigned_doctor = request.user
    interaction.save()
    from django.contrib import messages

    messages.success(request, "Case assigned. It will now appear in your dashboard.")
    return redirect("doctors:index")


@doctor_required
@require_POST
def add_note(request, interaction_id):
    """Add a note to a triage interaction."""
    interaction = get_object_or_404(TriageInteraction, id=interaction_id)
    note_text = request.POST.get("note", "").strip()
    if note_text:
        TriageDoctorNote.objects.create(
            interaction=interaction, doctor=request.user, note=note_text
        )
    return redirect("doctors:index")


@doctor_required
def triage_feed(request):
    """JSON feed of triage interactions for polling/updates."""
    from django.http import JsonResponse

    severity_order = models.Case(
        models.When(severity="Critical", then=4),
        models.When(severity="Severe", then=3),
        models.When(severity="Moderate", then=2),
        models.When(severity="Mild", then=1),
        default=0,
        output_field=models.IntegerField(),
    )

    interactions = (
        TriageInteraction.objects.select_related("user")
        .annotate(severity_rank=severity_order)
        .order_by("-severity_rank", "-updated_at")[:20]
    )

    data = [
        {
            "id": i.id,
            "severity": i.severity,
            "summary": i.result.get("summary", "") if i.result else "",
            "created_at": i.created_at.isoformat(),
        }
        for i in interactions
    ]
    return JsonResponse({"interactions": data})


@doctor_required
def triage_pdf(request, interaction_id):
    """Generate and download a PDF for a triage interaction."""
    if canvas is None:
        from django.http import HttpResponseBadRequest

        return HttpResponseBadRequest("PDF generation not available. Install reportlab.")

    interaction = get_object_or_404(TriageInteraction, id=interaction_id)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="triage-{interaction.id}.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, "Triage Report")

    # Patient info
    y = height - 100
    p.setFont("Helvetica", 12)
    p.drawString(50, y, f"Patient: {interaction.user.get_full_name() or interaction.user.username}")
    y -= 20
    p.drawString(50, y, f"Date: {interaction.created_at.strftime('%Y-%m-%d %H:%M')}")
    y -= 20
    p.drawString(50, y, f"Severity: {interaction.severity or 'Not specified'}")

    # Result summary
    if interaction.result:
        y -= 40
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, y, "Summary")
        y -= 20
        p.setFont("Helvetica", 10)
        summary = interaction.result.get("summary", "")
        for line in summary.split("\n"):
            if y < 100:
                p.showPage()
                y = height - 50
            p.drawString(50, y, line[:80])
            y -= 15

    p.save()
    return response
