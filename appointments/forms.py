from django import forms
from django.utils import timezone


class AppointmentBookingForm(forms.Form):
    """Form for booking a new appointment."""

    doctor = forms.ModelChoiceField(
        queryset=None,  # Will be set in __init__
        widget=forms.Select(attrs={"class": "form-select"}),
        help_text="Select a doctor",
    )
    appointment_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control",
            }
        ),
        help_text="Select appointment date",
    )
    appointment_time = forms.TimeField(
        widget=forms.TimeInput(
            attrs={
                "type": "time",
                "class": "form-control",
                "step": "900",  # 15 minute intervals
            }
        ),
        help_text="Select appointment time",
    )
    reason = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Describe your symptoms or reason for the appointment...",
            }
        ),
        required=False,
        help_text="Reason for appointment (optional)",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show doctors in the dropdown
        from django.contrib.auth.models import User

        doctors = User.objects.filter(
            patient_profile__role="doctor"
        ).order_by("username")
        self.fields["doctor"].queryset = doctors
        
        # Set min date for appointment_date field
        self.fields["appointment_date"].widget.attrs["min"] = timezone.now().date().isoformat()

    def clean_appointment_date(self):
        """Validate that appointment date is not in the past."""
        date = self.cleaned_data.get("appointment_date")
        if date and date < timezone.now().date():
            raise forms.ValidationError("Appointment date cannot be in the past.")
        return date

    def clean(self):
        """Validate appointment date and time combination."""
        cleaned_data = super().clean()
        appointment_date = cleaned_data.get("appointment_date")
        appointment_time = cleaned_data.get("appointment_time")

        if appointment_date and appointment_time:
            # Check if appointment is in the past
            appointment_datetime = timezone.make_aware(
                timezone.datetime.combine(appointment_date, appointment_time)
            )
            if appointment_datetime < timezone.now():
                raise forms.ValidationError(
                    "Appointment date and time cannot be in the past."
                )

        return cleaned_data


class AppointmentUpdateForm(forms.Form):
    """Form for updating appointment notes (for doctors)."""

    notes = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Add notes about this appointment...",
            }
        ),
        required=False,
        help_text="Doctor notes",
    )

