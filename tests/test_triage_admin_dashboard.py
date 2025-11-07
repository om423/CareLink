import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from triage.models import TriageInteraction


@pytest.mark.django_db
def test_dashboard_access_requires_staff(client):
    """Test that non-staff users cannot access the admin dashboard."""
    User.objects.create_user("alice", password="pass12345")
    client.login(username="alice", password="pass12345")
    r = client.get(reverse("triage:admin_dashboard"))
    # Should redirect to login or return 403
    assert r.status_code in (302, 403)


@pytest.mark.django_db
def test_dashboard_access_allows_staff(client):
    """Test that staff users can access the admin dashboard."""
    User.objects.create_user("doc", password="pass12345", is_staff=True)
    client.login(username="doc", password="pass12345")
    r = client.get(reverse("triage:admin_dashboard"))
    assert r.status_code == 200
    assert "Incoming Triage Reports" in r.content.decode()


@pytest.mark.django_db
def test_dashboard_access_allows_superuser(client):
    """Test that superusers can access the admin dashboard."""
    User.objects.create_superuser(
        "admin", "admin@example.com", "pass12345"
    )
    client.login(username="admin", password="pass12345")
    r = client.get(reverse("triage:admin_dashboard"))
    assert r.status_code == 200
    assert "Incoming Triage Reports" in r.content.decode()


@pytest.mark.django_db
def test_dashboard_lists_interactions(client):
    """Test that dashboard displays triage interactions."""
    User.objects.create_user("doc", password="pass12345", is_staff=True)
    patient = User.objects.create_user("patient", password="pass12345")
    client.login(username="doc", password="pass12345")

    # Create a triage interaction
    TriageInteraction.objects.create(
        user=patient,
        symptoms_text="Headache and fever",
        severity="Critical",
        result={
            "summary": "Possible severe condition requiring immediate "
            "attention"
        }
    )

    r = client.get(reverse("triage:admin_dashboard"))
    assert r.status_code == 200
    content = r.content.decode()
    assert "Headache and fever" in content
    assert "Critical" in content
    assert "patient" in content


@pytest.mark.django_db
def test_dashboard_orders_by_severity(client):
    """Test that dashboard orders interactions by severity."""
    User.objects.create_user("doc", password="pass12345", is_staff=True)
    patient1 = User.objects.create_user("patient1", password="pass12345")
    patient2 = User.objects.create_user("patient2", password="pass12345")
    patient3 = User.objects.create_user("patient3", password="pass12345")

    client.login(username="doc", password="pass12345")

    # Create interactions with different severities
    TriageInteraction.objects.create(
        user=patient1,
        symptoms_text="Mild symptoms",
        severity="Mild",
        result={"summary": "Mild condition"}
    )
    TriageInteraction.objects.create(
        user=patient2,
        symptoms_text="Critical symptoms",
        severity="Critical",
        result={"summary": "Critical condition"}
    )
    TriageInteraction.objects.create(
        user=patient3,
        symptoms_text="Moderate symptoms",
        severity="Moderate",
        result={"summary": "Moderate condition"}
    )

    r = client.get(reverse("triage:admin_dashboard"))
    assert r.status_code == 200
    content = r.content.decode()

    # Find positions of each severity in the rendered HTML
    critical_pos = content.find("Critical symptoms")
    moderate_pos = content.find("Moderate symptoms")
    mild_pos = content.find("Mild symptoms")

    # Critical should appear first
    assert critical_pos != -1
    assert moderate_pos != -1
    assert mild_pos != -1
    assert critical_pos < moderate_pos
    assert moderate_pos < mild_pos


@pytest.mark.django_db
def test_dashboard_filter_by_severity(client):
    """Test that severity filter works correctly."""
    User.objects.create_user("doc", password="pass12345", is_staff=True)
    patient1 = User.objects.create_user("patient1", password="pass12345")
    patient2 = User.objects.create_user("patient2", password="pass12345")

    client.login(username="doc", password="pass12345")

    TriageInteraction.objects.create(
        user=patient1,
        symptoms_text="Critical symptoms",
        severity="Critical",
        result={"summary": "Critical condition"}
    )
    TriageInteraction.objects.create(
        user=patient2,
        symptoms_text="Mild symptoms",
        severity="Mild",
        result={"summary": "Mild condition"}
    )

    # Filter by Critical
    r = client.get(reverse("triage:admin_dashboard") + "?severity=Critical")
    assert r.status_code == 200
    content = r.content.decode()
    assert "Critical symptoms" in content
    assert "Mild symptoms" not in content

    # Filter by Mild
    r = client.get(reverse("triage:admin_dashboard") + "?severity=Mild")
    assert r.status_code == 200
    content = r.content.decode()
    assert "Mild symptoms" in content
    assert "Critical symptoms" not in content


@pytest.mark.django_db
def test_dashboard_shows_patient_info(client):
    """Test that dashboard displays patient name and email."""
    User.objects.create_user("doc", password="pass12345", is_staff=True)
    patient = User.objects.create_user(
        "patient",
        password="pass12345",
        email="patient@example.com",
        first_name="John",
        last_name="Doe"
    )
    client.login(username="doc", password="pass12345")

    TriageInteraction.objects.create(
        user=patient,
        symptoms_text="Test symptoms",
        severity="Moderate",
        result={"summary": "Test summary"}
    )

    r = client.get(reverse("triage:admin_dashboard"))
    assert r.status_code == 200
    content = r.content.decode()
    assert "John Doe" in content or "patient" in content
    assert "patient@example.com" in content


@pytest.mark.django_db
def test_dashboard_view_link_works(client):
    """Test that View button links to correct detail page."""
    User.objects.create_user("doc", password="pass12345", is_staff=True)
    patient = User.objects.create_user("patient", password="pass12345")
    client.login(username="doc", password="pass12345")

    interaction = TriageInteraction.objects.create(
        user=patient,
        symptoms_text="Test symptoms",
        severity="Moderate",
        result={"summary": "Test summary"}
    )

    r = client.get(reverse("triage:admin_dashboard"))
    assert r.status_code == 200
    content = r.content.decode()
    # Check that detail URL is present
    detail_url = reverse("triage:detail", args=[interaction.id])
    assert detail_url in content


@pytest.mark.django_db
def test_staff_can_view_any_patient_detail(client):
    """Test that staff can view any patient's triage detail."""
    User.objects.create_user("doc", password="pass12345", is_staff=True)
    patient = User.objects.create_user("patient", password="pass12345")
    client.login(username="doc", password="pass12345")

    interaction = TriageInteraction.objects.create(
        user=patient,
        symptoms_text="Patient symptoms",
        severity="Severe",
        result={"summary": "Patient summary"}
    )

    r = client.get(reverse("triage:detail", args=[interaction.id]))
    assert r.status_code == 200
    content = r.content.decode()
    assert "Patient symptoms" in content

