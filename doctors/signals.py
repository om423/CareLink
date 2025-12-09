"""Signals for doctors app."""

from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import DoctorProfile
from .utils import geocode_location


@receiver(pre_save, sender=DoctorProfile)
def geocode_clinic_address(sender, instance, **kwargs):
    """
    Automatically geocode clinic address when it's updated.
    Only geocodes if address has changed and coordinates are missing.
    """
    if instance.pk:  # Only for existing instances
        try:
            old_instance = DoctorProfile.objects.get(pk=instance.pk)
            # Check if address has changed
            if old_instance.clinic_address != instance.clinic_address:
                # Address changed, geocode it
                if instance.clinic_address:
                    lat, lon = geocode_location(instance.clinic_address)
                    if lat is not None and lon is not None:
                        instance.clinic_latitude = lat
                        instance.clinic_longitude = lon
        except DoctorProfile.DoesNotExist:
            # New instance, geocode if address is provided
            if instance.clinic_address:
                lat, lon = geocode_location(instance.clinic_address)
                if lat is not None and lon is not None:
                    instance.clinic_latitude = lat
                    instance.clinic_longitude = lon
    else:
        # New instance, geocode if address is provided
        if instance.clinic_address:
            lat, lon = geocode_location(instance.clinic_address)
            if lat is not None and lon is not None:
                instance.clinic_latitude = lat
                instance.clinic_longitude = lon
