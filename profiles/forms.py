from django import forms

from profiles.models import PatientProfile


class ProfileForm(forms.ModelForm):
    """Form for editing patient profile."""

    class Meta:
        model = PatientProfile
        fields = ("age", "weight", "medical_history", "allergies")
        widgets = {
            "age": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Age in years"}
            ),
            "weight": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Weight in kg", "step": "0.01"}
            ),
            "medical_history": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Previous medical conditions and history",
                }
            ),
            "allergies": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": ("Known allergies (medications, foods, environmental)"),
                }
            ),
        }
