from django import forms

from triage.models import TriageDoctorNote


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
