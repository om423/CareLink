from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class TriageInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="triage_interactions")
    session_id = models.CharField(
        max_length=255, blank=True, null=True, help_text="Unique identifier for chat session"
    )
    symptoms_text = models.TextField()
    severity = models.CharField(max_length=20, blank=True, null=True)
    result = models.JSONField(blank=True, null=True)
    assigned_doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="assigned_triage_interactions",
        help_text="Doctor/admin assigned to follow up on this triage report",
    )
    doctor_notes = models.TextField(
        blank=True, null=True, help_text="Professional notes or feedback from doctor/admin"
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="triage_reviews",
        help_text="Doctor/admin who reviewed this triage report",
    )
    reviewed_at = models.DateTimeField(
        null=True, blank=True, help_text="Timestamp when doctor notes were last updated"
    )
    review_status = models.CharField(
        max_length=20,
        choices=[
            ("pending_review", "Pending Review"),
            ("under_review", "Under Review"),
            ("finished_review", "Finished Review"),
        ],
        default="pending_review",
        help_text="Current status of the triage review process",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self) -> str:
        return (
            f"TriageInteraction(user={self.user.username}, "
            f"severity={self.severity}, "
            f"at={self.created_at:%Y-%m-%d %H:%M})"
        )

    def severity_rank(self):
        """Return numeric rank for severity ordering (higher = more urgent)."""
        levels = {"Critical": 4, "Severe": 3, "Moderate": 2, "Mild": 1}
        return levels.get(self.severity, 0)

    def has_doctor_notes(self):
        """Check if doctor notes exist and are not empty."""
        return bool(self.doctor_notes and self.doctor_notes.strip())


class TriageDoctorNote(models.Model):
    interaction = models.ForeignKey(
        TriageInteraction,
        on_delete=models.CASCADE,
        related_name="notes",
        help_text="Triage interaction this note belongs to",
    )
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="triage_notes",
        help_text="Doctor/admin who wrote the note",
    )
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Triage Doctor Note"
        verbose_name_plural = "Triage Doctor Notes"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Note by {self.doctor.username} on {self.interaction.id} at {self.created_at:%Y-%m-%d %H:%M}"
