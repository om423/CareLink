import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import models, transaction
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

from .forms import DoctorAvailabilityFormSet, DoctorProfileForm
from .models import DoctorAvailability, DoctorProfile


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
    """Find a doctor page with map view - only accessible to patients."""
    from profiles.models import PatientProfile

    from .models import DoctorProfile
    from .utils import calculate_distance, geocode_location

    # Get all doctors with coordinates
    doctors_with_coords = DoctorProfile.objects.filter(
        clinic_latitude__isnull=False, clinic_longitude__isnull=False
    )

    # Prepare doctor data for the map
    doctors_data = []
    for doctor in doctors_with_coords:
        doctors_data.append(
            {
                "id": doctor.id,
                "name": doctor.user.get_full_name() or doctor.user.username,
                "specialty": doctor.specialty,
                "clinic_name": doctor.clinic_name,
                "clinic_address": doctor.clinic_address,
                "latitude": float(doctor.clinic_latitude),
                "longitude": float(doctor.clinic_longitude),
                "consultation_fee": float(doctor.consultation_fee),
                "years_of_experience": doctor.years_of_experience,
                "url": f"/doctors/{doctor.id}/",  # Future detail page
            }
        )

    # Get user's location from profile if available
    user_lat = None
    user_lon = None
    user_location = None
    max_distance = request.GET.get("distance", "all")  # Default to 'all' to show all doctors

    try:
        patient_profile = PatientProfile.objects.get(user=request.user)
        # Get location from profile if available
        if patient_profile.latitude and patient_profile.longitude:
            user_lat = float(patient_profile.latitude)
            user_lon = float(patient_profile.longitude)
            user_location = patient_profile.address
        elif patient_profile.address:
            # Try to geocode if address exists but coordinates don't
            try:
                lat, lon = geocode_location(patient_profile.address)
                if lat is not None and lon is not None:
                    patient_profile.latitude = lat
                    patient_profile.longitude = lon
                    patient_profile.save(update_fields=["latitude", "longitude"])
                    user_lat = float(lat)
                    user_lon = float(lon)
                    user_location = patient_profile.address
            except Exception:
                pass
    except PatientProfile.DoesNotExist:
        pass

    # Calculate distances if user location is available (for display, not filtering)
    # Frontend will handle filtering based on distance selector
    if user_lat and user_lon:
        for doctor_data in doctors_data:
            distance = calculate_distance(
                user_lat, user_lon, doctor_data["latitude"], doctor_data["longitude"]
            )
            doctor_data["distance"] = round(distance, 1)
        # Sort by distance for better UX
        doctors_data.sort(key=lambda x: x.get("distance", float("inf")))
    else:
        # Sort by clinic name if no user location
        doctors_data.sort(key=lambda x: x["clinic_name"])

    # Don't filter on backend - let frontend JavaScript handle filtering
    # This ensures all doctors are available for the map, and filtering happens client-side

    # Convert doctors_data to JSON-safe format
    doctors_data_json = json.dumps(doctors_data)

    context = {
        "doctors_data": doctors_data_json,
        "doctors_count": len(doctors_data),
        "user_lat": user_lat,
        "user_lon": user_lon,
        "max_distance": max_distance,
        "user_location": user_location,
    }
    return render(request, "doctors/find_doctor.html", context)


@login_required
def doctor_detail(request, doctor_id):
    """View doctor profile details - accessible to all logged-in users."""
    doctor_profile = get_object_or_404(DoctorProfile, id=doctor_id)
    doctor_user = doctor_profile.user

    # Get availability
    availability = DoctorAvailability.objects.filter(
        doctor=doctor_profile, is_available=True
    ).order_by("day_of_week", "start_time")

    # Calculate distance if patient has location
    distance = None
    if request.user.is_authenticated:
        try:
            from profiles.models import PatientProfile

            from .utils import calculate_distance

            patient_profile = PatientProfile.objects.get(user=request.user)
            if (
                patient_profile.latitude
                and patient_profile.longitude
                and doctor_profile.clinic_latitude
                and doctor_profile.clinic_longitude
            ):
                distance = calculate_distance(
                    float(patient_profile.latitude),
                    float(patient_profile.longitude),
                    float(doctor_profile.clinic_latitude),
                    float(doctor_profile.clinic_longitude),
                )
                distance = round(distance, 1)
        except Exception:
            pass

    # Check if user can book appointments (patients only)
    can_book = False
    try:
        from accounts.views import get_user_role

        role = get_user_role(request.user)
        can_book = role == "patient"
    except Exception:
        pass

    context = {
        "doctor_profile": doctor_profile,
        "doctor_user": doctor_user,
        "availability": availability,
        "distance": distance,
        "can_book": can_book,
    }
    return render(request, "doctors/detail.html", context)


@doctor_required
def manage_availability(request):
    """View to manage doctor's profile and availability schedule."""
    # Get or create the DoctorProfile for the current user
    # Provide defaults for non-nullable fields to avoid IntegrityError on creation
    defaults = {
        "specialty": "General Practice",
        "clinic_name": "My Clinic",
        "clinic_address": "123 Main St",
        "consultation_fee": 100.00,
        "years_of_experience": 0,
    }
    profile, created = DoctorProfile.objects.get_or_create(user=request.user, defaults=defaults)

    if created:
        messages.info(
            request, "A new profile has been created for you. Please update your details."
        )

    if request.method == "POST":
        profile_form = DoctorProfileForm(request.POST, request.FILES, instance=profile)
        formset = DoctorAvailabilityFormSet(request.POST, instance=profile)

        if profile_form.is_valid() and formset.is_valid():
            with transaction.atomic():
                profile_form.save()
                formset.save()
            messages.success(request, "Profile and availability updated successfully.")
            return redirect("doctors:manage_availability")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        profile_form = DoctorProfileForm(instance=profile)
        # If no availabilities exist, create default Mon-Fri 9-5
        if not profile.availabilities.exists():
            initial_data = []
            for day in range(7):
                initial_data.append(
                    {
                        "day_of_week": day,
                        "start_time": "09:00",
                        "end_time": "17:00",
                        "is_available": day < 5,  # Mon-Fri
                    }
                )
            # Use extra to show the forms, but we need to handle this carefully
            # For now, let's just create the objects if they don't exist
            # to simplify the formset usage
            for data in initial_data:
                DoctorAvailability.objects.create(doctor=profile, **data)

        formset = DoctorAvailabilityFormSet(instance=profile)

    context = {
        "profile_form": profile_form,
        "formset": formset,
    }
    return render(request, "doctors/manage_availability.html", context)


@doctor_required
@require_POST
def assign_to_self(request, interaction_id):
    """Assign a triage interaction to the current doctor."""
    interaction = get_object_or_404(TriageInteraction, id=interaction_id)
    interaction.assigned_doctor = request.user
    interaction.save()
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
