from django.db import models
from django.contrib.auth.models import User


class PatientProfile(models.Model):
    """User profile model storing role and medical information."""
    
    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor/Admin'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='patient',
        help_text="User role: Patient or Doctor/Admin"
    )
    age = models.PositiveIntegerField(null=True, blank=True, help_text="Patient's age in years")
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Weight in kg")
    medical_history = models.TextField(blank=True, help_text="Previous medical conditions and history")
    allergies = models.TextField(blank=True, help_text="Known allergies (medications, foods, environmental)")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Patient Profile'
        verbose_name_plural = 'Patient Profiles'
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def is_patient(self):
        """Check if user is a patient."""
        return self.role == 'patient'
    
    def is_doctor(self):
        """Check if user is a doctor/admin."""
        return self.role == 'doctor'
