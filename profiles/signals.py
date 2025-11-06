from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from profiles.models import PatientProfile


@receiver(post_save, sender=User)
def create_patient_profile(sender, instance, created, **kwargs):
    """Automatically create PatientProfile when a new User is created."""
    if created:
        PatientProfile.objects.get_or_create(user=instance, defaults={'role': 'patient'})

