import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from triage.models import TriageInteraction


@pytest.mark.django_db
def test_staff_can_add_notes(client):
    """Test that staff users can add notes to triage reports."""
    staff = User.objects.create_user("doc", password="pass", is_staff=True)
    patient = User.objects.create_user("pat", password="pass")
    triage = TriageInteraction.objects.create(
        user=patient, severity="Moderate", symptoms_text="Headache", result={"summary": "Test"}
    )

    client.login(username="doc", password="pass")
    url = reverse("triage:update_doctor_notes", args=[triage.id])
    res = client.post(url, {"doctor_notes": "Follow up in 2 days"})
    assert res.status_code == 200
    assert res.json()["success"] is True
    triage.refresh_from_db()
    assert triage.doctor_notes == "Follow up in 2 days"
    assert triage.reviewed_by == staff
    assert triage.reviewed_at is not None


@pytest.mark.django_db
def test_patient_cannot_add_notes(client):
    """Test that patients cannot add notes to triage reports."""
    user = User.objects.create_user("pat", password="pass")
    triage = TriageInteraction.objects.create(
        user=user, severity="Mild", symptoms_text="Cough", result={"summary": "ok"}
    )
    client.login(username="pat", password="pass")
    res = client.post(
        reverse("triage:update_doctor_notes", args=[triage.id]), {"doctor_notes": "X"}
    )
    assert res.status_code in (302, 403)


@pytest.mark.django_db
def test_notes_update_timestamp(client):
    """Test that updating notes updates reviewed_at timestamp."""
    User.objects.create_user("doc", password="pass", is_staff=True)
    patient = User.objects.create_user("pat", password="pass")
    triage = TriageInteraction.objects.create(
        user=patient, severity="Moderate", symptoms_text="Test", result={"summary": "Test"}
    )

    client.login(username="doc", password="pass")
    url = reverse("triage:update_doctor_notes", args=[triage.id])

    # First update
    res1 = client.post(url, {"doctor_notes": "Initial notes"})
    assert res1.status_code == 200
    triage.refresh_from_db()
    first_timestamp = triage.reviewed_at

    # Second update
    res2 = client.post(url, {"doctor_notes": "Updated notes"})
    assert res2.status_code == 200
    triage.refresh_from_db()
    second_timestamp = triage.reviewed_at

    assert second_timestamp > first_timestamp
    assert triage.doctor_notes == "Updated notes"


@pytest.mark.django_db
def test_has_doctor_notes_method(client):
    """Test the has_doctor_notes model method."""
    patient = User.objects.create_user("pat", password="pass")
    triage = TriageInteraction.objects.create(
        user=patient, severity="Moderate", symptoms_text="Test", result={"summary": "Test"}
    )

    assert triage.has_doctor_notes() is False

    triage.doctor_notes = "Some notes"
    triage.save()
    assert triage.has_doctor_notes() is True

    triage.doctor_notes = "   "
    triage.save()
    assert triage.has_doctor_notes() is False


@pytest.mark.django_db
def test_patients_can_view_notes(client):
    """Test that patients can view doctor notes in read-only mode."""
    staff = User.objects.create_user("doc", password="pass", is_staff=True)
    patient = User.objects.create_user("pat", password="pass")
    triage = TriageInteraction.objects.create(
        user=patient,
        severity="Moderate",
        symptoms_text="Test symptoms",
        result={"summary": "Test summary"},
        doctor_notes="Follow up recommended",
        reviewed_by=staff,
    )

    client.login(username="pat", password="pass")
    res = client.get(reverse("triage:detail", args=[triage.id]))
    assert res.status_code == 200
    content = res.content.decode()
    assert "Follow up recommended" in content
    assert "Doctor Notes" in content
