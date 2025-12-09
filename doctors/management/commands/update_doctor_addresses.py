"""Management command to update all doctors with unique addresses."""

import time

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from doctors.models import DoctorProfile
from doctors.utils import geocode_location


class Command(BaseCommand):
    help = "Update all doctors with unique clinic addresses and geocode them"

    def handle(self, *args, **options):
        # Map of usernames to unique addresses spread across Atlanta area
        doctor_addresses = {
            "gautam": {
                "clinic_name": "Valiveti Medical Center",
                "clinic_address": "3200 Downwood Cir NW, Atlanta, GA 30327",
                "specialty": "General Practice",
                "consultation_fee": 120.00,
            },
            "huz": {
                "clinic_name": "My Clinic",
                "clinic_address": "1000 Johnson Ferry Rd NE, Atlanta, GA 30342",
                "specialty": "General Practice",
                "consultation_fee": 100.00,
            },
            "luv": {
                "clinic_name": "Luvielmo Family Practice",
                "clinic_address": "550 Peachtree St NE, Atlanta, GA 30308",
                "specialty": "General Practice",
                "consultation_fee": 110.00,
            },
            "ritwij": {
                "clinic_name": "Ghosh Medical Associates",
                "clinic_address": "1365 Clifton Rd NE, Atlanta, GA 30322",
                "specialty": "General Practice",
                "consultation_fee": 115.00,
            },
            "rlafeldt2": {
                "clinic_name": "Raphael Clinic",
                "clinic_address": "1405 Clifton Rd NE, Atlanta, GA 30322",
                "specialty": "General Practice",
                "consultation_fee": 100.00,
            },
            "sidkumar": {
                "clinic_name": "Kumar Healthcare Center",
                "clinic_address": "12 Executive Park Dr NE, Atlanta, GA 30329",
                "specialty": "General Practice",
                "consultation_fee": 125.00,
            },
            "varsha": {
                "clinic_name": "Kantheti Medical Practice",
                "clinic_address": "1841 Clifton Rd NE, Atlanta, GA 30329",
                "specialty": "General Practice",
                "consultation_fee": 105.00,
            },
        }

        updated_count = 0
        geocoded_count = 0

        for username, data in doctor_addresses.items():
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"User {username} not found, skipping..."))
                continue

            # Get or create doctor profile
            doctor_profile, created = DoctorProfile.objects.get_or_create(
                user=user,
                defaults={
                    "specialty": data["specialty"],
                    "clinic_name": data["clinic_name"],
                    "clinic_address": data["clinic_address"],
                    "consultation_fee": data["consultation_fee"],
                    "years_of_experience": 10,  # Default
                    "bio": f'Experienced {data["specialty"]} physician.',
                },
            )

            # Update if it already existed
            if not created:
                doctor_profile.specialty = data["specialty"]
                doctor_profile.clinic_name = data["clinic_name"]
                doctor_profile.clinic_address = data["clinic_address"]
                doctor_profile.consultation_fee = data["consultation_fee"]
                if not doctor_profile.bio:
                    doctor_profile.bio = f'Experienced {data["specialty"]} physician.'
                doctor_profile.save()
                self.stdout.write(f"Updated profile for {username}")

            # Geocode if coordinates are missing or address changed
            needs_geocoding = (
                not doctor_profile.clinic_latitude
                or not doctor_profile.clinic_longitude
                or doctor_profile.clinic_address == data["clinic_address"]
            )

            if needs_geocoding:
                time.sleep(1)  # Rate limiting
                lat, lon = geocode_location(doctor_profile.clinic_address)
                if lat is not None and lon is not None:
                    doctor_profile.clinic_latitude = lat
                    doctor_profile.clinic_longitude = lon
                    doctor_profile.save()
                    geocoded_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"  ✓ Geocoded {doctor_profile.clinic_name}: " f"({lat}, {lon})"
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f"  ✗ Failed to geocode: {doctor_profile.clinic_name}")
                    )

            updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"\n✓ Updated {updated_count} doctor profiles\n"
                f"✓ Geocoded {geocoded_count} clinic addresses"
            )
        )
