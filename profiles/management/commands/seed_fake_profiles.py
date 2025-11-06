from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth.models import User
from decimal import Decimal
import random

from profiles.models import PatientProfile

try:
    from faker import Faker
except Exception:  # pragma: no cover
    Faker = None


SAMPLE_HISTORIES = [
    "Asthma since childhood; managed with inhaled corticosteroids. Two ER visits in past 5 years.",
    "Type 2 diabetes diagnosed 2018; on metformin. Mild neuropathy symptoms.",
    "Hypertension diagnosed 2020; controlled on lisinopril. No CV events.",
    "Hypothyroidism on levothyroxine. Routine labs stable last 12 months.",
    "Seasonal allergic rhinitis; uses antihistamines PRN. No prior hospitalizations.",
    "History of migraine headaches; triptan as needed. Triggers include stress and lack of sleep.",
]

SAMPLE_ALLERGIES = [
    "Penicillin (rash)",
    "Peanuts (hives)",
    "No known drug allergies",
    "Shellfish (swelling)",
    "Latex (contact dermatitis)",
    "Dust mites",
]


class Command(BaseCommand):
    help = "Seed fake medical history and allergies for patient profiles (safe test data)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--overwrite",
            action="store_true",
            help="Overwrite existing medical_history/allergies if already present",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        overwrite = options.get("overwrite", False)

        faker = Faker() if Faker else None
        updated = 0
        created = 0

        # Ensure each user has a PatientProfile; then seed fields
        users = User.objects.all().select_related("patient_profile")
        for user in users:
            profile, was_created = PatientProfile.objects.get_or_create(
                user=user,
                defaults={"role": "patient"},
            )
            if was_created:
                created += 1

            if profile.role != "patient":
                # Only seed patient profiles
                continue

            need_history = overwrite or not bool(profile.medical_history.strip())
            need_allergies = overwrite or not bool(profile.allergies.strip())

            if not (need_history or need_allergies):
                continue

            fields_to_update = ["updated_at"]

            if need_history:
                if faker:
                    profile.medical_history = faker.random_element(SAMPLE_HISTORIES)
                else:
                    profile.medical_history = SAMPLE_HISTORIES[updated % len(SAMPLE_HISTORIES)]
                fields_to_update.append("medical_history")

            if need_allergies:
                if faker:
                    profile.allergies = faker.random_element(SAMPLE_ALLERGIES)
                else:
                    profile.allergies = SAMPLE_ALLERGIES[updated % len(SAMPLE_ALLERGIES)]
                fields_to_update.append("allergies")

            # Derive plausible age and weight ranges from history
            history_lower = (profile.medical_history or "").lower()
            age_min, age_max = 18, 85
            wt_min, wt_max = 50, 100

            if "diabetes" in history_lower:
                age_min, age_max = 40, 75
                wt_min, wt_max = 70, 120
            elif "hypertension" in history_lower:
                age_min, age_max = 35, 80
                wt_min, wt_max = 65, 115
            elif "asthma" in history_lower:
                age_min, age_max = 18, 45
                wt_min, wt_max = 50, 90
            elif "hypothyroidism" in history_lower:
                age_min, age_max = 25, 70
                wt_min, wt_max = 55, 105
            elif "migraine" in history_lower:
                age_min, age_max = 20, 55
                wt_min, wt_max = 50, 95
            elif "allergic rhinitis" in history_lower or "allergic" in history_lower:
                age_min, age_max = 18, 65
                wt_min, wt_max = 50, 100

            # Set age/weight only if missing or overwrite requested
            if overwrite or profile.age is None:
                profile.age = int(random.randint(age_min, age_max))
                fields_to_update.append("age")
            if overwrite or profile.weight is None:
                weight_val = round(random.uniform(wt_min, wt_max), 1)
                profile.weight = Decimal(str(weight_val))
                fields_to_update.append("weight")

            profile.save(update_fields=list(set(fields_to_update)))
            updated += 1

        self.stdout.write(self.style.SUCCESS(
            f"Profiles ensured: {users.count()}, newly created: {created}, updated with fake data: {updated}"
        ))


