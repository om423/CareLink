from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class DoctorProfile(models.Model):
    """Profile model for doctors storing professional and clinic details."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="doctor_profile"
    )
    specialty = models.CharField(
        max_length=100, help_text=_("Medical specialty (e.g., General Practice, Cardiology)")
    )
    bio = models.TextField(blank=True, help_text=_("Professional biography and background"))
    clinic_name = models.CharField(max_length=200, help_text=_("Name of the clinic or hospital"))
    clinic_address = models.TextField(help_text=_("Physical address of the clinic"))
    clinic_latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        help_text=_("Clinic latitude coordinate"),
    )
    clinic_longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        help_text=_("Clinic longitude coordinate"),
    )
    consultation_fee = models.DecimalField(
        max_digits=10, decimal_places=2, help_text=_("Standard consultation fee")
    )
    years_of_experience = models.PositiveIntegerField(
        default=0, help_text=_("Years of medical practice")
    )
    profile_image = models.ImageField(
        upload_to="doctors/profiles/",
        null=True,
        blank=True,
        help_text=_("Doctor's profile picture"),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} - {self.specialty}"


class DoctorAvailability(models.Model):
    """Model to store doctor's weekly schedule availability."""

    DAYS_OF_WEEK = [
        (0, _("Monday")),
        (1, _("Tuesday")),
        (2, _("Wednesday")),
        (3, _("Thursday")),
        (4, _("Friday")),
        (5, _("Saturday")),
        (6, _("Sunday")),
    ]

    doctor = models.ForeignKey(
        DoctorProfile, on_delete=models.CASCADE, related_name="availabilities"
    )
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK, help_text=_("Day of the week"))
    start_time = models.TimeField(help_text=_("Shift start time"), null=True, blank=True)
    end_time = models.TimeField(help_text=_("Shift end time"), null=True, blank=True)
    is_available = models.BooleanField(
        default=True, help_text=_("Whether the doctor is available on this day")
    )

    class Meta:
        ordering = ["day_of_week", "start_time"]
        verbose_name = _("Doctor Availability")
        verbose_name_plural = _("Doctor Availabilities")
        constraints = [
            models.UniqueConstraint(
                fields=["doctor", "day_of_week"], name="unique_doctor_day_availability"
            )
        ]

    def __str__(self):
        day_name = dict(self.DAYS_OF_WEEK).get(self.day_of_week, "Unknown")
        return f"{self.doctor} - {day_name} ({self.start_time} - {self.end_time})"
