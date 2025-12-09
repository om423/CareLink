"""Management command to seed fake doctor profiles with clinic locations."""

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from doctors.models import DoctorAvailability, DoctorProfile
from doctors.utils import geocode_location


class Command(BaseCommand):
    help = "Create fake doctor profiles with clinic locations for testing"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=10,
            help="Number of fake doctors to create (default: 10)",
        )

    def handle(self, *args, **options):
        count = options["count"]

        # Sample doctor data with real clinic addresses in major US cities
        doctor_data = [
            {
                "username": "dr_smith",
                "first_name": "John",
                "last_name": "Smith",
                "email": "dr.smith@carelink.com",
                "specialty": "General Practice",
                "clinic_name": "Atlanta Medical Center",
                "clinic_address": "1365 Clifton Rd NE, Atlanta, GA 30322",
                "consultation_fee": 150.00,
                "years_of_experience": 15,
                "bio": "Board-certified family physician with 15 years of experience.",
            },
            {
                "username": "dr_johnson",
                "first_name": "Sarah",
                "last_name": "Johnson",
                "email": "s.johnson@carelink.com",
                "specialty": "Cardiology",
                "clinic_name": "Heart Care Clinic",
                "clinic_address": "550 Peachtree St NE, Atlanta, GA 30308",
                "consultation_fee": 250.00,
                "years_of_experience": 20,
                "bio": "Cardiologist specializing in preventive heart care.",
            },
            {
                "username": "dr_williams",
                "first_name": "Michael",
                "last_name": "Williams",
                "email": "m.williams@carelink.com",
                "specialty": "Pediatrics",
                "clinic_name": "Children's Health Center",
                "clinic_address": "1405 Clifton Rd NE, Atlanta, GA 30322",
                "consultation_fee": 120.00,
                "years_of_experience": 12,
                "bio": "Pediatrician dedicated to children's health and wellness.",
            },
            {
                "username": "dr_brown",
                "first_name": "Emily",
                "last_name": "Brown",
                "email": "e.brown@carelink.com",
                "specialty": "Dermatology",
                "clinic_name": "Skin Care Specialists",
                "clinic_address": "5673 Peachtree Dunwoody Rd, Atlanta, GA 30342",
                "consultation_fee": 200.00,
                "years_of_experience": 10,
                "bio": "Dermatologist with expertise in skin conditions and cosmetic procedures.",
            },
            {
                "username": "dr_davis",
                "first_name": "David",
                "last_name": "Davis",
                "email": "d.davis@carelink.com",
                "specialty": "Orthopedics",
                "clinic_name": "Orthopedic Care Center",
                "clinic_address": "1000 Johnson Ferry Rd NE, Atlanta, GA 30342",
                "consultation_fee": 300.00,
                "years_of_experience": 18,
                "bio": "Orthopedic surgeon specializing in joint and bone health.",
            },
            {
                "username": "dr_miller",
                "first_name": "Jennifer",
                "last_name": "Miller",
                "email": "j.miller@carelink.com",
                "specialty": "Internal Medicine",
                "clinic_name": "Internal Medicine Associates",
                "clinic_address": "3200 Downwood Cir NW, Atlanta, GA 30327",
                "consultation_fee": 180.00,
                "years_of_experience": 14,
                "bio": "Internal medicine physician focused on adult health.",
            },
            {
                "username": "dr_wilson",
                "first_name": "Robert",
                "last_name": "Wilson",
                "email": "r.wilson@carelink.com",
                "specialty": "Neurology",
                "clinic_name": "Neurological Institute",
                "clinic_address": "12 Executive Park Dr NE, Atlanta, GA 30329",
                "consultation_fee": 280.00,
                "years_of_experience": 22,
                "bio": "Neurologist with expertise in brain and nervous system disorders.",
            },
            {
                "username": "dr_moore",
                "first_name": "Lisa",
                "last_name": "Moore",
                "email": "l.moore@carelink.com",
                "specialty": "Obstetrics & Gynecology",
                "clinic_name": "Women's Health Center",
                "clinic_address": "5669 Peachtree Dunwoody Rd, Atlanta, GA 30342",
                "consultation_fee": 220.00,
                "years_of_experience": 16,
                "bio": "OB/GYN providing comprehensive women's healthcare.",
            },
            {
                "username": "dr_taylor",
                "first_name": "James",
                "last_name": "Taylor",
                "email": "j.taylor@carelink.com",
                "specialty": "Psychiatry",
                "clinic_name": "Mental Health Associates",
                "clinic_address": "1841 Clifton Rd NE, Atlanta, GA 30329",
                "consultation_fee": 250.00,
                "years_of_experience": 19,
                "bio": "Psychiatrist specializing in mental health and wellness.",
            },
            {
                "username": "dr_anderson",
                "first_name": "Patricia",
                "last_name": "Anderson",
                "email": "p.anderson@carelink.com",
                "specialty": "Emergency Medicine",
                "clinic_name": "Emergency Care Clinic",
                "clinic_address": "5315 Peachtree Industrial Blvd, Atlanta, GA 30341",
                "consultation_fee": 200.00,
                "years_of_experience": 11,
                "bio": "Emergency medicine physician providing urgent care services.",
            },
        ]

        created_count = 0
        geocoded_count = 0

        for i, data in enumerate(doctor_data[:count]):
            # Create or get user
            user, user_created = User.objects.get_or_create(
                username=data["username"],
                defaults={
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                    "email": data["email"],
                },
            )

            if user_created:
                user.set_password("password123")
                user.save()
                self.stdout.write(f"Created user: {data['username']}")

            # Create or update doctor profile
            doctor_profile, profile_created = DoctorProfile.objects.get_or_create(
                user=user,
                defaults={
                    "specialty": data["specialty"],
                    "bio": data["bio"],
                    "clinic_name": data["clinic_name"],
                    "clinic_address": data["clinic_address"],
                    "consultation_fee": data["consultation_fee"],
                    "years_of_experience": data["years_of_experience"],
                },
            )

            # Update clinic address if it changed
            if doctor_profile.clinic_address != data["clinic_address"]:
                doctor_profile.clinic_address = data["clinic_address"]
                doctor_profile.save()

            # Geocode if coordinates are missing
            if not doctor_profile.clinic_latitude or not doctor_profile.clinic_longitude:
                import time

                time.sleep(1)  # Rate limiting delay
                lat, lon = geocode_location(doctor_profile.clinic_address)
                if lat is not None and lon is not None:
                    doctor_profile.clinic_latitude = lat
                    doctor_profile.clinic_longitude = lon
                    doctor_profile.save()
                    geocoded_count += 1
                    self.stdout.write(
                        f"  Geocoded: {doctor_profile.clinic_name} -> " f"({lat}, {lon})"
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f"  Failed to geocode: {doctor_profile.clinic_name}")
                    )

            if profile_created:
                created_count += 1
                self.stdout.write(
                    f"Created doctor profile: Dr. {data['first_name']} "
                    f"{data['last_name']} - {data['specialty']}"
                )

                # Create default availability (Mon-Fri 9-5)
                for day in range(5):  # Monday to Friday
                    DoctorAvailability.objects.create(
                        doctor=doctor_profile,
                        day_of_week=day,
                        start_time="09:00",
                        end_time="17:00",
                        is_available=True,
                    )

        # Also geocode any existing doctors without coordinates
        existing_doctors = (
            DoctorProfile.objects.filter(
                clinic_latitude__isnull=True, clinic_longitude__isnull=True
            )
            .exclude(clinic_address__isnull=True)
            .exclude(clinic_address="")
        )

        import time

        for doctor in existing_doctors:
            # Update addresses that are too generic
            if doctor.clinic_address in ["123 Main St", "My street is this one"]:
                # Update with a real Atlanta address
                doctor.clinic_address = "1000 Johnson Ferry Rd NE, Atlanta, GA 30342"
                doctor.save()

            time.sleep(1)  # Rate limiting delay
            lat, lon = geocode_location(doctor.clinic_address)
            if lat is not None and lon is not None:
                doctor.clinic_latitude = lat
                doctor.clinic_longitude = lon
                doctor.save()
                geocoded_count += 1
                self.stdout.write(
                    f"Geocoded existing doctor: {doctor.clinic_name} -> " f"({lat}, {lon})"
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Failed to geocode existing doctor: {doctor.clinic_name}")
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSuccessfully created {created_count} new doctor profiles "
                f"and geocoded {geocoded_count} clinic addresses."
            )
        )
