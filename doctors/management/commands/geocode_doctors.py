"""Management command to geocode doctor clinic addresses."""

from django.core.management.base import BaseCommand

from doctors.utils import geocode_doctor_locations


class Command(BaseCommand):
    help = "Geocode all doctor clinic addresses that don't have coordinates yet"

    def handle(self, *args, **options):
        self.stdout.write("Starting geocoding of doctor clinic addresses...")
        count = geocode_doctor_locations()
        self.stdout.write(
            self.style.SUCCESS(f"Successfully geocoded {count} doctor clinic addresses.")
        )
