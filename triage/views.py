from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import JsonResponse
from django.db import models
import json

from carelink.common.services.gemini_client import GeminiClient
from .models import TriageInteraction
from accounts.views import patient_required

try:
    from profiles.models import PatientProfile
except Exception:
    PatientProfile = None


def index(request):
    return render(request, "triage/index.html")


@patient_required
def history(request):
    """View triage history for the current user - one entry per chat session. Patients only."""
    # Get unique sessions (latest interaction per session_id)
    # For interactions without session_id, each one is treated as a separate session
    from django.db.models import Max

    # Get the latest interaction ID for each session
    latest_interactions = (
        TriageInteraction.objects
        .filter(user=request.user)
        .values('session_id')
        .annotate(latest_id=Max('id'))
        .values_list('latest_id', flat=True)
    )

    # Get those interactions
    interactions = (
        TriageInteraction.objects
        .filter(id__in=latest_interactions)
        .order_by('-updated_at')
    )

    return render(request, "triage/history.html", {"interactions": interactions})


@login_required
def detail(request, interaction_id):
    """View details of a specific triage interaction."""
    from django.shortcuts import get_object_or_404

    # Allow staff/admin or doctors to view any patient's triage
    can_view_all = False
    if request.user.is_staff or request.user.is_superuser:
        can_view_all = True
    else:
        # Check if user has doctor role
        try:
            if PatientProfile is not None:
                profile = PatientProfile.objects.get(user=request.user)
                if profile.role == 'doctor':
                    can_view_all = True
        except Exception:
            pass

    if can_view_all:
        interaction = get_object_or_404(
            TriageInteraction, id=interaction_id
        )
    else:
        interaction = get_object_or_404(
            TriageInteraction, id=interaction_id, user=request.user
        )
    return render(request, "triage/detail.html", {"interaction": interaction})


def get_patient_context(user):
    """Helper to get patient context for triage."""
    patient_ctx = {}
    if PatientProfile is not None:
        try:
            prof = PatientProfile.objects.get(user=user)
            patient_ctx = {
                "age": getattr(prof, "age", None),
                "weight": float(getattr(prof, "weight", 0)) if getattr(prof, "weight", None) is not None else None,
                "medical_history": (getattr(prof, "medical_history", None) or "")[:300] or None,
                "allergies": (getattr(prof, "allergies", None) or "")[:200] or None,
            }
        except Exception:
            patient_ctx = {}
    return patient_ctx


@patient_required
def chat(request):
    """Main chat view - renders the chat page. Patients only."""
    patient_ctx = get_patient_context(request.user)
    return render(request, "triage/chat.html", {"patient_ctx": patient_ctx})


@patient_required
def chat_api(request):
    """API endpoint for submitting symptoms and getting AI response (AJAX)."""
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    # Parse JSON body
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    symptoms = (body.get("symptoms") or "").strip()
    conversation_history = body.get("conversation_history", [])
    session_id = body.get("session_id")

    if not symptoms:
        return JsonResponse({"error": "Please describe your symptoms."}, status=400)

    api_key = getattr(settings, "GEMINI_API_KEY", None)
    client = GeminiClient(api_key=api_key)
    patient_ctx = get_patient_context(request.user)

    try:
        # Build full conversation context by combining history with current symptoms
        all_symptoms = []
        for item in conversation_history:
            if item.get("role") == "user":
                all_symptoms.append(item.get("content", ""))
        all_symptoms.append(symptoms)

        # Combine all symptoms for comprehensive assessment
        combined_symptoms = (
            "\n\nAdditional information: ".join(all_symptoms)
        )

        result = client.generate_triage(
            combined_symptoms, patient_context=patient_ctx
        )

        # Persist or update interaction with full context based on session_id
        try:
            if session_id:
                # Try to find existing interaction for this session
                interaction, created = TriageInteraction.objects.get_or_create(
                    user=request.user,
                    session_id=session_id,
                    defaults={
                        'symptoms_text': combined_symptoms,
                        'severity': result.get("severity"),
                        'result': result,
                    }
                )
                # If interaction already exists, update it with latest information
                if not created:
                    interaction.symptoms_text = combined_symptoms
                    interaction.severity = result.get("severity")
                    interaction.result = result
                    interaction.save()
            else:
                # Fallback if no session_id provided
                TriageInteraction.objects.create(
                    user=request.user,
                    symptoms_text=combined_symptoms,
                    severity=result.get("severity"),
                    result=result,
                )
        except Exception:
            # non-fatal; do not block UI if persistence fails
            pass

        return JsonResponse({
            "success": True,
            "result": result
        })
    except RuntimeError as e:
        return JsonResponse({"error": str(e)}, status=500)
    except Exception as e:
        return JsonResponse({
            "error": f"Sorry — something went wrong generating your preliminary assessment: {e}"
        }, status=500)


@staff_member_required
def admin_dashboard(request):
    """Doctor/Admin dashboard to view and prioritize incoming triage reports."""
    # Order by severity rank (Critical → Severe → Moderate → Mild) then by recency
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
        .order_by("-severity_rank", "-updated_at")
    )

    # Optional filter by severity level
    filter_level = request.GET.get("severity")
    if filter_level:
        interactions = interactions.filter(severity=filter_level)

    context = {
        "interactions": interactions,
        "filter_level": filter_level,
        "severity_levels": ["Critical", "Severe", "Moderate", "Mild"],
    }
    return render(request, "triage/admin_dashboard.html", context)
