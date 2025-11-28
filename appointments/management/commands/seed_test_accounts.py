"""
Management command to seed the database with test accounts (patients and doctors).
Usage: python manage.py seed_test_accounts
"""
import random
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction

from profiles.models import PatientProfile

# Sample medical data
SAMPLE_HISTORIES = [
    "Asthma since childhood; managed with inhaled corticosteroids.",
    "Type 2 diabetes diagnosed 2018; on metformin.",
    "Hypertension diagnosed 2020; controlled on lisinopril.",
    "Hypothyroidism on levothyroxine. Routine labs stable.",
    "Seasonal allergic rhinitis; uses antihistamines PRN.",
    "History of migraine headaches; triptan as needed.",
    "No significant medical history.",
    "Previous knee surgery in 2019. Full recovery.",
    "Mild anxiety, managed with therapy.",
    "High cholesterol, diet controlled.",
]

SAMPLE_ALLERGIES = [
    "Penicillin (rash)",
    "Peanuts (hives)",
    "No known drug allergies",
    "Shellfish (swelling)",
    "Latex (contact dermatitis)",
    "Dust mites",
    "Aspirin (stomach upset)",
]

# Patient names
PATIENT_NAMES = [
    ("Alice", "Johnson"),
    ("Bob", "Smith"),
    ("Carol", "Williams"),
    ("David", "Brown"),
    ("Emma", "Jones"),
    ("Frank", "Garcia"),
    ("Grace", "Miller"),
    ("Henry", "Davis"),
    ("Ivy", "Rodriguez"),
    ("Jack", "Martinez"),
    ("Kate", "Hernandez"),
    ("Liam", "Lopez"),
    ("Mia", "Wilson"),
    ("Noah", "Anderson"),
    ("Olivia", "Thomas"),
    ("Paul", "Taylor"),
    ("Quinn", "Moore"),
    ("Rachel", "Jackson"),
    ("Sam", "Martin"),
    ("Tina", "Lee"),
    ("Uma", "Thompson"),
    ("Victor", "White"),
    ("Wendy", "Harris"),
    ("Xavier", "Sanchez"),
    ("Yara", "Clark"),
    ("Zoe", "Ramirez"),
    ("Alex", "Lewis"),
    ("Blake", "Robinson"),
    ("Casey", "Walker"),
    ("Dana", "Young"),
]

# Doctor names
DOCTOR_NAMES = [
    ("Dr. Sarah", "Chen", "Cardiologist"),
    ("Dr. Michael", "Patel", "Pediatrician"),
    ("Dr. Jennifer", "Kim", "Dermatologist"),
    ("Dr. Robert", "Singh", "Orthopedist"),
    ("Dr. Lisa", "Anderson", "Neurologist"),
    ("Dr. James", "Wilson", "Psychiatrist"),
    ("Dr. Maria", "Gonzalez", "Gynecologist"),
    ("Dr. David", "Taylor", "Oncologist"),
    ("Dr. Emily", "Brown", "Endocrinologist"),
    ("Dr. Christopher", "Lee", "Pulmonologist"),
    ("Dr. Amanda", "White", "Gastroenterologist"),
    ("Dr. Daniel", "Martinez", "Urologist"),
    ("Dr. Jessica", "Johnson", "Rheumatologist"),
    ("Dr. Matthew", "Davis", "Ophthalmologist"),
    ("Dr. Nicole", "Miller", "ENT Specialist"),
]


class Command(BaseCommand):
    help = "Seed database with test accounts (patients and doctors) for testing appointment functionality."

    def add_arguments(self, parser):
        parser.add_argument(
            "--patients",
            type=int,
            default=30,
            help="Number of patient accounts to create (default: 30)",
        )
        parser.add_argument(
            "--doctors",
            type=int,
            default=15,
            help="Number of doctor accounts to create (default: 15)",
        )
        parser.add_argument(
            "--password",
            type=str,
            default="test123",
            help="Password for all test accounts (default: test123)",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        num_patients = options["patients"]
        num_doctors = options["doctors"]
        password = options["password"]

        self.stdout.write(self.style.SUCCESS("Creating test accounts..."))
        self.stdout.write(f"Patients: {num_patients}, Doctors: {num_doctors}")
        self.stdout.write("=" * 60)

        # Create patients
        patients_created = []
        for i in range(min(num_patients, len(PATIENT_NAMES))):
            first_name, last_name = PATIENT_NAMES[i]
            username = f"patient{i+1:02d}_{first_name.lower()}"
            email = f"{username}@test.com"

            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                },
            )

            if created:
                user.set_password(password)
                user.save()

                # Create patient profile
                profile, _ = PatientProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        "role": "patient",
                        "age": random.randint(18, 80),
                        "weight": Decimal(str(round(random.uniform(50, 100), 1))),
                        "medical_history": random.choice(SAMPLE_HISTORIES),
                        "allergies": random.choice(SAMPLE_ALLERGIES),
                        "onboarding_completed": True,
                    },
                )
                patients_created.append((username, password, "patient"))
                self.stdout.write(
                    self.style.SUCCESS(f"✓ Created patient: {username} / {password}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"⚠ Patient {username} already exists")
                )

        # Create doctors
        doctors_created = []
        for i in range(min(num_doctors, len(DOCTOR_NAMES))):
            first_name, last_name, specialty = DOCTOR_NAMES[i]
            username = f"doctor{i+1:02d}_{last_name.lower()}"
            email = f"{username}@test.com"

            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "first_name": first_name,
                    "last_name": f"{last_name} ({specialty})",
                    "email": email,
                },
            )

            if created:
                user.set_password(password)
                user.save()

                # Create or update doctor profile
                profile, created = PatientProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        "role": "doctor",
                        "onboarding_completed": True,
                    },
                )
                # Ensure role is set to doctor even if profile already existed
                if not created or profile.role != "doctor":
                    profile.role = "doctor"
                    profile.onboarding_completed = True
                    profile.save()
                doctors_created.append((username, password, "doctor"))
                self.stdout.write(
                    self.style.SUCCESS(f"✓ Created doctor: {username} / {password}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"⚠ Doctor {username} already exists")
                )

        # Print summary
        self.stdout.write("")
        self.stdout.write("=" * 60)
        self.stdout.write(self.style.SUCCESS("SUMMARY"))
        self.stdout.write("=" * 60)
        self.stdout.write(f"Total Patients Created: {len(patients_created)}")
        self.stdout.write(f"Total Doctors Created: {len(doctors_created)}")
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("PATIENT ACCOUNTS:"))
        for username, pwd, role in patients_created:
            self.stdout.write(f"  {username:30s} / {pwd} ({role})")
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("DOCTOR ACCOUNTS:"))
        for username, pwd, role in doctors_created:
            self.stdout.write(f"  {username:30s} / {pwd} ({role})")
        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"All accounts use password: {password}\n"
                "You can now test appointment booking functionality!"
            )
        )

