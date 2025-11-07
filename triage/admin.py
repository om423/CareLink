from django.contrib import admin
from .models import TriageInteraction


@admin.register(TriageInteraction)
class TriageInteractionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "severity",
        "has_doctor_notes",
        "reviewed_by",
        "created_at"
    )
    list_filter = ("severity", "created_at", "reviewed_at")
    search_fields = ("user__username", "symptoms_text", "doctor_notes")
    readonly_fields = ("created_at", "updated_at", "reviewed_at")
    fieldsets = (
        ("Patient Information", {
            "fields": ("user", "session_id")
        }),
        ("Triage Data", {
            "fields": ("symptoms_text", "severity", "result")
        }),
        ("Doctor Review", {
            "fields": (
                "doctor_notes",
                "reviewed_by",
                "reviewed_at"
            )
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        })
    )
