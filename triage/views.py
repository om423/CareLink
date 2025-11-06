from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages

from carelink.common.services.gemini_client import GeminiClient
from .models import TriageInteraction

try:
    from profiles.models import PatientProfile
except Exception:
    PatientProfile = None

def index(request):
    return render(request, "triage/index.html")


@login_required
def chat(request):
    result = None
    api_key = getattr(settings, "GEMINI_API_KEY", None)
    client = GeminiClient(api_key=api_key)

    # Build context from user profile (optional)
    patient_ctx = {}
    if PatientProfile is not None:
        try:
            prof = PatientProfile.objects.get(user=request.user)
            patient_ctx = {
                "age": getattr(prof, "age", None),
                "weight": float(getattr(prof, "weight", 0)) if getattr(prof, "weight", None) is not None else None,
                "medical_history": (getattr(prof, "medical_history", None) or "")[:300] or None,
                "allergies": (getattr(prof, "allergies", None) or "")[:200] or None,
            }
        except Exception:
            patient_ctx = {}

    submitted_symptoms = None
    if request.method == "POST":
        symptoms = (request.POST.get("symptoms") or "").strip()
        if not symptoms:
            messages.error(request, "Please describe your symptoms.")
        else:
            try:
                submitted_symptoms = symptoms
                result = client.generate_triage(symptoms, patient_context=patient_ctx)
                # persist interaction
                try:
                    TriageInteraction.objects.create(
                        user=request.user,
                        symptoms_text=symptoms,
                        severity=result.get("severity"),
                        result=result,
                    )
                except Exception:
                    # non-fatal; do not block UI if persistence fails
                    pass
            except RuntimeError as e:
                messages.error(request, str(e))
            except Exception as e:
                messages.error(request, f"Sorry — something went wrong generating your preliminary assessment: {e}")

    return render(request, "triage/chat.html", {"result": result, "submitted_symptoms": submitted_symptoms, "patient_ctx": patient_ctx})
