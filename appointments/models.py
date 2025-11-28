from django.conf import settings
from django.db import models
from django.utils import timezone


class Appointment(models.Model):
    """Appointment model for booking doctor visits."""

    STATUS_CHOICES = [
        ("pending", "Scheduled"),
        ("confirmed", "Confirmed"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    APPOINTMENT_TYPE_CHOICES = [
        ("in_person", "In Person"),
        ("virtual", "Virtual Visit"),
    ]

    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="patient_appointments",
        help_text="Patient who booked the appointment",
    )
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="doctor_appointments",
        help_text="Doctor assigned to the appointment",
    )
    appointment_date = models.DateField(help_text="Date of the appointment")
    appointment_time = models.TimeField(help_text="Time of the appointment")
    appointment_type = models.CharField(
        max_length=20,
        choices=APPOINTMENT_TYPE_CHOICES,
        default="in_person",
        help_text="Type of appointment: in-person or virtual",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        help_text="Current status of the appointment",
    )
    reason = models.TextField(
        blank=True,
        help_text="Reason for the appointment or symptoms",
    )
    notes = models.TextField(
        blank=True,
        help_text="Additional notes from patient or doctor",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-appointment_date", "-appointment_time"]
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"

    def __str__(self):
        return (
            f"Appointment: {self.patient.username} with "
            f"{self.doctor.username} on {self.appointment_date} at {self.appointment_time}"
        )

    def is_past(self):
        """Check if appointment is in the past."""
        appointment_datetime = timezone.make_aware(
            timezone.datetime.combine(self.appointment_date, self.appointment_time)
        )
        return appointment_datetime < timezone.now()

    def can_be_cancelled(self):
        """Check if appointment can be cancelled."""
        return self.status in ["pending", "confirmed"] and not self.is_past()

    def can_be_edited(self):
        """Check if appointment can be edited."""
        # Allow editing of pending or confirmed appointments
        # (validation for past appointments will be handled in the form)
        return self.status in ["pending", "confirmed"]
