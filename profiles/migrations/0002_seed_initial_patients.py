from django.db import migrations
from django.contrib.auth.hashers import make_password


def seed_initial_patients(apps, schema_editor):
    User = apps.get_model("auth", "User")
    PatientProfile = apps.get_model("profiles", "PatientProfile")

    seed_data = [
        {
            "username": "john_doe",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "age": 34,
            "weight": "78.5",
            "medical_history": "Seasonal allergies; mild asthma",
            "allergies": "Penicillin",
        },
        {
            "username": "jane_smith",
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane@example.com",
            "age": 28,
            "weight": "62.3",
            "medical_history": "No chronic conditions",
            "allergies": "None",
        },
        {
            "username": "michael_b",
            "first_name": "Michael",
            "last_name": "Brown",
            "email": "michael@example.com",
            "age": 47,
            "weight": "85.0",
            "medical_history": "Hypertension; hyperlipidemia",
            "allergies": "NSAIDs",
        },
        {
            "username": "emily_r",
            "first_name": "Emily",
            "last_name": "Rose",
            "email": "emily@example.com",
            "age": 19,
            "weight": "55.8",
            "medical_history": "Iron deficiency (past)",
            "allergies": "Peanuts",
        },
        {
            "username": "david_k",
            "first_name": "David",
            "last_name": "King",
            "email": "david@example.com",
            "age": 61,
            "weight": "90.4",
            "medical_history": "Type 2 diabetes; GERD",
            "allergies": "Sulfa drugs",
        },
    ]

    for rec in seed_data:
        user, _ = User.objects.get_or_create(
            username=rec["username"],
            defaults={
                "first_name": rec["first_name"],
                "last_name": rec["last_name"],
                "email": rec["email"],
            },
        )
        # ensure a usable password for demo (set hashed directly in migration)
        user.password = make_password("carelink123")
        user.save(update_fields=["password"])

        PatientProfile.objects.update_or_create(
            user=user,
            defaults={
                "role": "patient",
                "age": rec["age"],
                "weight": rec["weight"],
                "medical_history": rec["medical_history"],
                "allergies": rec["allergies"],
            },
        )


def unseed_initial_patients(apps, schema_editor):
    User = apps.get_model("auth", "User")
    usernames = ["john_doe", "jane_smith", "michael_b", "emily_r", "david_k"]
    User.objects.filter(username__in=usernames).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0001_initial"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.RunPython(seed_initial_patients, reverse_code=unseed_initial_patients),
    ]


