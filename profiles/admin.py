from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils import timezone
import csv
from profiles.models import PatientProfile


class PatientProfileInline(admin.StackedInline):
    """Inline admin for PatientProfile."""
    model = PatientProfile
    can_delete = False
    verbose_name_plural = 'Patient Profile'
    fields = ('role', 'age', 'weight', 'medical_history', 'allergies', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')


class CustomUserAdmin(UserAdmin):
    """Custom User admin with PatientProfile inline."""
    inlines = (PatientProfileInline,)
    list_display = (
        'username', 'email', 'first_name', 'last_name',
        'is_staff', 'is_superuser', 'is_active',
        'get_user_role', 'date_joined'
    )
    list_filter = (
        'is_staff', 'is_superuser', 'is_active',
        'date_joined', 'groups'
    )
    search_fields = ('username', 'first_name', 'last_name', 'email')
    actions = ['export_users_csv']

    def get_user_role(self, obj):
        try:
            return obj.patient_profile.get_role_display()
        except PatientProfile.DoesNotExist:
            return 'No Profile'
    get_user_role.short_description = 'Role'

    @admin.action(description='Export selected users to CSV')
    def export_users_csv(self, request, queryset):
        """Export selected users to CSV file."""
        response = HttpResponse(content_type='text/csv')
        timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
        response['Content-Disposition'] = (
            f'attachment; filename="users_export_{timestamp}.csv"'
        )

        writer = csv.writer(response)
        writer.writerow([
            'Username', 'Email', 'First Name', 'Last Name', 'Role',
            'Is Staff', 'Is Superuser', 'Is Active', 'Date Joined',
            'Last Login', 'Age', 'Weight', 'Medical History', 'Allergies'
        ])

        for user in queryset:
            try:
                profile = user.patient_profile
                role = profile.get_role_display()
                age = profile.age if profile.age else 'N/A'
                weight = profile.weight if profile.weight else 'N/A'
                med_history = (
                    profile.medical_history[:50]
                    if profile.medical_history else 'N/A'
                )
                allergies = (
                    profile.allergies[:50]
                    if profile.allergies else 'N/A'
                )
            except PatientProfile.DoesNotExist:
                role = age = weight = med_history = allergies = 'No Profile'

            writer.writerow([
                user.username,
                user.email,
                user.first_name,
                user.last_name,
                role,
                user.is_staff,
                user.is_superuser,
                user.is_active,
                user.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
                (
                    user.last_login.strftime('%Y-%m-%d %H:%M:%S')
                    if user.last_login else 'Never'
                ),
                age,
                weight,
                med_history,
                allergies
            ])

        return response


@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    """Admin for PatientProfile."""
    list_display = ('user', 'role', 'age', 'weight', 'created_at', 'updated_at')
    list_filter = ('role', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email', 'medical_history', 'allergies')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'role')
        }),
        ('Medical Information', {
            'fields': ('age', 'weight', 'medical_history', 'allergies')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    actions = ['export_profiles_csv']

    @admin.action(description='Export selected profiles to CSV')
    def export_profiles_csv(self, request, queryset):
        """Export selected profiles to CSV file."""
        response = HttpResponse(content_type='text/csv')
        timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
        response['Content-Disposition'] = (
            f'attachment; filename="profiles_export_{timestamp}.csv"'
        )

        writer = csv.writer(response)
        writer.writerow([
            'Username', 'User Email', 'Age', 'Weight',
            'Medical History', 'Allergies', 'Created At', 'Updated At'
        ])

        for profile in queryset:
            writer.writerow([
                profile.user.username,
                profile.user.email,
                profile.age if profile.age else 'N/A',
                profile.weight if profile.weight else 'N/A',
                profile.medical_history if profile.medical_history else 'N/A',
                profile.allergies if profile.allergies else 'N/A',
                profile.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                profile.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            ])

        return response


# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Group is already registered by Django admin by default
