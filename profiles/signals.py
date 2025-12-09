"""Signals for profiles app."""

import time

from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import PatientProfile


@receiver(pre_save, sender=PatientProfile)
def geocode_patient_address(sender, instance, **kwargs):
    """
    Automatically geocode patient address when it's updated.
    Geocodes if address has changed or coordinates are missing.
    """
    # Only geocode if address is provided
    if not instance.address:
        return

    # Check if we need to geocode
    should_geocode = False

    if instance.pk:  # Existing instance
        try:
            old_instance = PatientProfile.objects.get(pk=instance.pk)
            # Geocode if address changed or coordinates are missing
            if (
                old_instance.address != instance.address
                or not instance.latitude
                or not instance.longitude
            ):
                should_geocode = True
        except PatientProfile.DoesNotExist:
            # Instance doesn't exist yet, geocode if coordinates missing
            if not instance.latitude or not instance.longitude:
                should_geocode = True
    else:
        # New instance, geocode if coordinates missing
        if not instance.latitude or not instance.longitude:
            should_geocode = True

    if should_geocode:
        try:
            from doctors.utils import geocode_location

            time.sleep(0.5)  # Rate limiting
            lat, lon = geocode_location(instance.address)
            if lat is not None and lon is not None:
                instance.latitude = lat
                instance.longitude = lon
        except ImportError:
            pass
        except Exception:
            # Silently fail if geocoding doesn't work
            pass
