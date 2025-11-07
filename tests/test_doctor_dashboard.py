import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from profiles.models import PatientProfile
from triage.models import TriageDoctorNote, TriageInteraction


def _create_user(username: str, role: str = "patient") -> User:
    user = User.objects.create_user(username, password="pass12345", first_name=username.title())
    profile, _created = PatientProfile.objects.get_or_create(user=user)
    profile.role = role
    profile.save()
    return user


@pytest.mark.django_db
def test_doctor_dashboard_lists_unassigned_cases(client):
    _create_user("house", role="doctor")
    patient = _create_user("patient-one")

    TriageInteraction.objects.create(
        user=patient,
        severity="Severe",
        symptoms_text="High fever, chest discomfort",
        result={
            "severity": "Severe",
            "summary": "Signs concerning for severe infection",
            "advice": "Seek urgent in-person evaluation",
            "red_flags": ["Chest pain", "High fever"],
            "differential": ["Pneumonia"],
            "rationale": "Multiple red flags reported",
        },
    )

    client.login(username="house", password="pass12345")
    response = client.get(reverse("doctors:index"))

    assert response.status_code == 200
    priority_queue = response.context["priority_queue"]
    assert len(priority_queue) == 1
    assert priority_queue[0].result["summary"] == "Signs concerning for severe infection"
    assert priority_queue[0].severity == "Severe"


@pytest.mark.django_db
def test_doctor_can_assign_case_to_self(client):
    doctor = _create_user("strange", role="doctor")
    patient = _create_user("patient-two")

    interaction = TriageInteraction.objects.create(
        user=patient,
        severity="Critical",
        symptoms_text="Severe shortness of breath",
        result={
            "severity": "Critical",
            "summary": "Respiratory distress suspected",
            "advice": "Call emergency services",
            "red_flags": ["Shortness of breath"],
            "differential": ["Pulmonary embolism"],
            "rationale": "Acute respiratory compromise",
        },
    )

    client.login(username="strange", password="pass12345")
    assign_url = reverse("doctors:assign_to_self", args=[interaction.id])
    response = client.post(assign_url, follow=True)

    assert response.status_code == 200
    interaction.refresh_from_db()
    assert interaction.assigned_doctor == doctor

    html = response.content.decode()
    assert "Case assigned. It will now appear in your dashboard." in html


@pytest.mark.django_db
def test_doctor_notes_visible_to_all_doctors(client):
    doctor_one = _create_user("doogie", role="doctor")
    _create_user("meredith", role="doctor")
    patient = _create_user("patient-three")

    interaction = TriageInteraction.objects.create(
        user=patient,
        severity="Moderate",
        symptoms_text="Migraine headaches",
        result={
            "severity": "Moderate",
            "summary": "Likely migraine recurrence",
            "advice": "Track triggers and follow neurology plan",
            "red_flags": [],
            "differential": ["Migraine"],
            "rationale": "History consistent with migraines",
        },
        assigned_doctor=doctor_one,
    )

    client.login(username="doogie", password="pass12345")
    note_url = reverse("doctors:add_note", args=[interaction.id])
    client.post(note_url, {"note": "Schedule tele-visit within 48 hours."})

    note = TriageDoctorNote.objects.get(interaction=interaction)
    assert note.note.startswith("Schedule")
    assert note.doctor == doctor_one

    client.logout()
    client.login(username="meredith", password="pass12345")
    response = client.get(reverse("doctors:index"))

    assert response.status_code == 200
    team_cases = response.context["team_cases"]
    assert len(team_cases) == 1
    case = team_cases[0]
    assert case.assigned_doctor == doctor_one
    assert list(case.notes.all())[0].note == "Schedule tele-visit within 48 hours."


@pytest.mark.django_db
def test_triage_feed_partial_updates(client):
    _create_user("poller", role="doctor")
    patient = _create_user("patient-feed")

    TriageInteraction.objects.create(
        user=patient,
        severity="Mild",
        symptoms_text="Seasonal allergies",
        result={
            "severity": "Mild",
            "summary": "Likely seasonal allergic rhinitis",
            "advice": "OTC antihistamines and hydration",
            "red_flags": [],
            "differential": ["Allergic rhinitis"],
            "rationale": "Symptoms align with allergies",
        },
    )

    client.login(username="poller", password="pass12345")
    response = client.get(reverse("doctors:triage_feed"))

    assert response.status_code == 200
    content = response.content.decode()
    assert "Seasonal allergies" not in content  # symptoms_text not shown
    assert "Likely seasonal allergic rhinitis" in content


@pytest.mark.django_db
def test_triage_pdf_download(client):
    _create_user("downloads", role="doctor")
    patient = _create_user("patient-pdf")

    interaction = TriageInteraction.objects.create(
        user=patient,
        severity="Critical",
        symptoms_text="Severe abdominal pain",
        result={
            "severity": "Critical",
            "summary": "Acute abdomen suspected",
            "advice": "Immediate emergency evaluation",
            "red_flags": ["Rebound tenderness"],
            "differential": ["Appendicitis"],
            "rationale": "Presentation suggests surgical emergency",
        },
    )

    client.login(username="downloads", password="pass12345")
    response = client.get(reverse("doctors:triage_pdf", args=[interaction.id]))

    assert response.status_code == 200
    assert response["Content-Type"] == "application/pdf"
    assert response["Content-Disposition"].startswith("attachment; filename=triage-")
