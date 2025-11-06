import pytest
from django.contrib.auth.models import User
from django.urls import reverse


@pytest.mark.django_db
def test_triage_chat_get_requires_login(client):
    r = client.get(reverse("triage:chat"))
    # should redirect to login
    assert r.status_code in (302, 301)


@pytest.mark.django_db
def test_triage_chat_post_monkeypatched(client, monkeypatch):
    user = User.objects.create_user("alice", password="pass12345")
    client.login(username="alice", password="pass12345")

    # Monkeypatch GeminiClient.generate_triage to avoid network
    from carelink.common.services import gemini_client

    captured_prompt = {"text": ""}

    original_build = gemini_client.GeminiClient._build_prompt

    def wrapper_build(self, s, patient_context=None):
        text = original_build(self, s, patient_context)
        captured_prompt["text"] = text
        return text

    def fake_generate(self, s, patient_context=None):
        # Ensure prompt is constructed for validation
        _ = self._build_prompt(s, patient_context=patient_context)
        return {
            "severity": "Moderate",
            "summary": "Possible viral upper respiratory infection.",
            "advice": "Hydration, rest; seek care if symptoms worsen.",
            "red_flags": ["Shortness of breath", "Chest pain"],
            "differential": ["Common cold", "Influenza"],
            "rationale": "Based on reported fever and sore throat.",
        }

    monkeypatch.setattr(gemini_client.GeminiClient, "_build_prompt", wrapper_build)
    monkeypatch.setattr(gemini_client.GeminiClient, "generate_triage", fake_generate)

    r = client.post(reverse("triage:chat"), {"symptoms": "fever and sore throat"})
    assert r.status_code == 200
    # ensure the rendered template contains expected strings
    content = r.content.decode()
    assert "Possible viral upper respiratory infection." in content
    assert "Moderate" in content
    assert "seek care if symptoms worsen" in content

    # Validate patient context labels appear in the prompt
    prompt = captured_prompt["text"]
    assert "PATIENT_CONTEXT" in prompt
    assert '"age":' in prompt
    assert '"weight":' in prompt
    assert '"allergies":' in prompt
    assert '"medical_history":' in prompt
    assert "PATIENT_SYMPTOM_DESCRIPTION" in prompt


class FakeResp:
    def __init__(self, text):
        self.text = text


@pytest.mark.django_db
def test_build_prompt_unknown_defaults(monkeypatch, settings):
    settings.GEMINI_API_KEY = "fake"
    from carelink.common.services.gemini_client import GeminiClient
    client = GeminiClient(api_key="fake")

    prompt = client._build_prompt("headache & nausea", patient_context={})
    assert 'PATIENT_CONTEXT' in prompt
    assert '"age": "Unknown"' in prompt
    assert '"weight": "Unknown"' in prompt
    assert '"allergies": "None reported"' in prompt
    assert '"medical_history": "None reported"' in prompt
    assert 'PATIENT_SYMPTOM_DESCRIPTION' in prompt
    assert 'headache & nausea' in prompt


@pytest.mark.django_db
def test_json_repair_flow(client, monkeypatch, settings):
    user = User.objects.create_user("cat", password="pass12345")
    client.login(username="cat", password="pass12345")
    settings.GEMINI_API_KEY = "fake"

    class FakeModel:
        calls = 0
        def generate_content(self, prompt):
            FakeModel.calls += 1
            if FakeModel.calls == 1:
                return FakeResp("```json\n{\"severity\":\"Moderate\",\"summary\":\"X\"\n```")
            else:
                return FakeResp('{"severity":"Mild","summary":"OK","advice":"Hydrate","red_flags":[],"differential":[],"rationale":"Repaired"}')

    from carelink.common.services import gemini_client
    # Patch new SDK path to use our fake model
    monkeypatch.setattr(gemini_client, "genai_new", type("GNew", (), {"Client": lambda api_key=None: type("C", (), {"models": type("M", (), {"generate_content": lambda self=None, model=None, contents=None: FakeModel().generate_content("")})()})()}))
    # Skip sleep
    monkeypatch.setattr(gemini_client.time, "sleep", lambda s: None)

    r = client.post(reverse("triage:chat"), {"symptoms": "test"})
    assert r.status_code == 200
    html = r.content.decode()
    assert "Mild" in html
    assert "OK" in html


@pytest.mark.django_db
def test_transient_error_backoff(client, monkeypatch, settings):
    user = User.objects.create_user("dog", password="pass12345")
    client.login(username="dog", password="pass12345")
    settings.GEMINI_API_KEY = "fake"

    class FlakyModel:
        calls = 0
        def generate_content(self, prompt):
            FlakyModel.calls += 1
            if FlakyModel.calls == 1:
                raise Exception("Transient")
            return FakeResp('{"severity":"Severe","summary":"Y","advice":"See doctor","red_flags":[],"differential":[],"rationale":"ok"}')

    from carelink.common.services import gemini_client
    monkeypatch.setattr(gemini_client, "genai_new", type("GNew", (), {"Client": lambda api_key=None: type("C", (), {"models": type("M", (), {"generate_content": lambda self=None, model=None, contents=None: FlakyModel().generate_content("")})()})()}))
    monkeypatch.setattr(gemini_client.time, "sleep", lambda s: None)

    r = client.post(reverse("triage:chat"), {"symptoms": "test"})
    assert r.status_code == 200
    html = r.content.decode()
    assert "Severe" in html
    assert "Y" in html


@pytest.mark.django_db
def test_context_card_rendered(client, settings):
    user = User.objects.create_user("eve", password="pass12345")
    client.login(username="eve", password="pass12345")
    settings.GEMINI_API_KEY = None

    try:
        from profiles.models import PatientProfile
        PatientProfile.objects.create(
            user=user,
            age=44,
            weight="70.2",
            medical_history="T2DM",
            allergies="NSAIDs",
        )
    except Exception:
        pass

    r = client.get(reverse("triage:chat"))
    assert r.status_code == 200
    html = r.content.decode()
    assert "Context used" in html
