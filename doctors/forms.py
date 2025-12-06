from django import forms
from django.forms import inlineformset_factory

from triage.models import TriageDoctorNote
from .models import DoctorProfile, DoctorAvailability


class TriageDoctorNoteForm(forms.ModelForm):
    note = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 3, "class": "form-control", "placeholder": "Add a professional note"}
        ),
        label="",
    )

    class Meta:
        model = TriageDoctorNote
        fields = ["note"]


class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = [
            "specialty",
            "bio",
            "clinic_name",
            "clinic_address",
            "consultation_fee",
            "years_of_experience",
            "profile_image",
        ]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4}),
            "clinic_address": forms.Textarea(attrs={"rows": 2}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, (forms.CheckboxInput, forms.FileInput)):
                field.widget.attrs.update({"class": "form-control"})
            if isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({"class": "form-control-file"})


class DoctorAvailabilityForm(forms.ModelForm):
    class Meta:
        model = DoctorAvailability
        fields = ["day_of_week", "start_time", "end_time", "is_available"]
        widgets = {
            "start_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "end_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "day_of_week": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make start_time and end_time not required initially
        self.fields['start_time'].required = False
        self.fields['end_time'].required = False

    def clean(self):
        cleaned_data = super().clean()
        is_available = cleaned_data.get('is_available')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if is_available:
            if not start_time:
                self.add_error('start_time', 'Start time is required when available.')
            if not end_time:
                self.add_error('end_time', 'End time is required when available.')
        else:
            # If not available, we can ignore time inputs or set them to null if nullable
            # Since model fields are not null, we might need to set dummy values or allow null in model
            # For now, let's just proceed. The model fields currently do not allow null,
            # so we must handle this.
            pass
        return cleaned_data


DoctorAvailabilityFormSet = inlineformset_factory(
    DoctorProfile,
    DoctorAvailability,
    form=DoctorAvailabilityForm,
    extra=0,
    max_num=7,
    can_delete=False,
)
