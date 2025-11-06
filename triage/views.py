from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
import json

from carelink.common.services.gemini_client import GeminiClient
from .models import TriageInteraction

try:
    from profiles.models import PatientProfile
except Exception:
    PatientProfile = None

def index(request):
    return render(request, "triage/index.html")


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


@login_required
def chat(request):
    """Main chat view - renders the chat page."""
    patient_ctx = get_patient_context(request.user)
    return render(request, "triage/chat.html", {"patient_ctx": patient_ctx})


@login_required
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
        combined_symptoms = "\n\nAdditional information: ".join(all_symptoms)

        result = client.generate_triage(combined_symptoms, patient_context=patient_ctx)

        # Persist interaction with full context
        try:
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
