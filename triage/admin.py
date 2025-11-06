from django.contrib import admin
from .models import TriageInteraction


@admin.register(TriageInteraction)
class TriageInteractionAdmin(admin.ModelAdmin):
    list_display = ("user", "severity", "created_at")
    list_filter = ("severity", "created_at")
    search_fields = ("user__username", "symptoms_text")

# Register your models here.
