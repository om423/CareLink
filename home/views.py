from django.shortcuts import render
from django.db.models import Max

def index(request):
    """Home page - shows dashboard for logged-in users, landing page for others."""
    if not request.user.is_authenticated:
        # Show marketing landing page for logged-out users
        return render(request, "home/landing.html")

    # Fetch user data for dashboard
    from triage.models import TriageInteraction
    from profiles.models import PatientProfile

    # Get user profile
    try:
        profile = PatientProfile.objects.get(user=request.user)
    except PatientProfile.DoesNotExist:
        profile = None

    # Get unique triage sessions (latest interaction per session)
    latest_interactions_ids = (
        TriageInteraction.objects
        .filter(user=request.user)
        .values('session_id')
        .annotate(latest_id=Max('id'))
        .values_list('latest_id', flat=True)
    )

    # Get recent triage interactions (last 3)
    recent_interactions = (
        TriageInteraction.objects
        .filter(id__in=latest_interactions_ids)
        .order_by('-updated_at')[:3]
    )

    # Get total count of triage sessions
    total_triages = len(latest_interactions_ids)

    # Get most recent interaction for stats
    last_interaction = recent_interactions.first() if recent_interactions else None

    # Check profile completeness
    profile_complete = False
    if profile:
        profile_complete = bool(
            profile.age and
            profile.weight and
            profile.onboarding_completed
        )

    context = {
        'profile': profile,
        'recent_interactions': recent_interactions,
        'total_triages': total_triages,
        'last_interaction': last_interaction,
        'profile_complete': profile_complete,
    }

    return render(request, "home/dashboard.html", context)
