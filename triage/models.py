from django.db import models
from django.contrib.auth.models import User


class TriageInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="triage_interactions")
    session_id = models.CharField(max_length=255, blank=True, null=True, help_text="Unique identifier for chat session")
    symptoms_text = models.TextField()
    severity = models.CharField(max_length=20, blank=True, null=True)
    result = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self) -> str:
        return f"TriageInteraction(user={self.user.username}, severity={self.severity}, at={self.created_at:%Y-%m-%d %H:%M})"

# Create your models here.
