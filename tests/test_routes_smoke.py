import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_home_ok(client):
    resp = client.get(reverse("home:index"))
    assert resp.status_code == 200


@pytest.mark.parametrize("path", [
    "/accounts/",
    "/profiles/",
    "/triage/",
    "/doctors/",
    "/appointments/",
    "/healthz/",
    "/readyz/",
])
def test_placeholders_ok(client, path):
    r = client.get(path)
    assert r.status_code in (200, 302)
