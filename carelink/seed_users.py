from django.contrib.auth.models import User
from profiles.models import PatientProfile


def seed_users():
    """Seed the database with test users and admin."""
    users = [
        ("Ritwij", "Ghosh"),
        ("Varsha", "Kantheti"),
        ("Om", "Patel"),
        ("Guilherme", "Luvielmo"),
        ("Raphael", "Lafeldt"),
    ]
    
    for first, last in users:
        username = f"{first.lower()}{last.lower()}"
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "first_name": first,
                "last_name": last,
                "email": f"{first.lower()}@example.com",
            }
        )
        if created:
            user.set_password("password123")
            user.save()
            PatientProfile.objects.get_or_create(user=user)
            print(f"Created user: {username}")
        else:
            print(f"User {username} already exists")
    
    # Create superuser
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@example.com", "admin123")
        print("Created superuser: admin")
    else:
        print("Superuser admin already exists")


if __name__ == "__main__":
    seed_users()
