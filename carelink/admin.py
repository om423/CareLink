from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta, datetime

from appointments.models import Appointment
from doctors.models import DoctorProfile
from profiles.models import PatientProfile
from triage.models import TriageInteraction


@staff_member_required
def admin_dashboard(request):
    """Admin dashboard for monitoring platform performance and user satisfaction."""
    now = timezone.now()
    today = now.date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # User Metrics
    total_users = PatientProfile.objects.count()
    total_patients = PatientProfile.objects.filter(role="patient").count()
    total_doctors = PatientProfile.objects.filter(role="doctor").count()
    
    # Active users (logged in or had activity in last 30 days)
    from django.contrib.auth.models import User
    
    # Convert date to datetime for comparison (will be reused below)
    month_ago_datetime = timezone.make_aware(datetime.combine(month_ago, datetime.min.time()))
    week_ago_datetime = timezone.make_aware(datetime.combine(week_ago, datetime.min.time()))
    
    # Get users who logged in recently (exclude None values)
    users_with_login = list(User.objects.filter(
        last_login__isnull=False,
        last_login__gte=month_ago_datetime
    ).values_list('id', flat=True))
    
    # Get users with triage activity
    users_with_triage = list(TriageInteraction.objects.filter(
        created_at__gte=month_ago_datetime
    ).values_list('user_id', flat=True).distinct())
    
    # Get users with appointment activity
    users_with_appointments = list(Appointment.objects.filter(
        created_at__gte=month_ago_datetime
    ).values_list('patient_id', flat=True).distinct())
    
    # Combine all active user IDs
    active_user_ids = set(users_with_login + users_with_triage + users_with_appointments)
    active_users = len(active_user_ids)
    
    # Onboarding completion
    onboarding_completed = PatientProfile.objects.filter(onboarding_completed=True).count()
    onboarding_rate = (onboarding_completed / total_users * 100) if total_users > 0 else 0
    
    # New users (this month)
    new_users_month = PatientProfile.objects.filter(created_at__gte=month_ago_datetime).count()
    new_users_week = PatientProfile.objects.filter(created_at__gte=week_ago_datetime).count()
    
    # Triage Metrics
    total_triages = TriageInteraction.objects.count()
    triages_this_month = TriageInteraction.objects.filter(created_at__gte=month_ago_datetime).count()
    triages_this_week = TriageInteraction.objects.filter(created_at__gte=week_ago_datetime).count()
    triages_today = TriageInteraction.objects.filter(created_at__date=today).count()
    
    # Triage severity distribution
    severity_dist = TriageInteraction.objects.values('severity').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Triage review metrics (user satisfaction indicator)
    triages_reviewed = TriageInteraction.objects.filter(review_status="finished_review").count()
    triage_review_rate = (triages_reviewed / total_triages * 100) if total_triages > 0 else 0
    
    triages_pending_review = TriageInteraction.objects.filter(review_status="pending_review").count()
    triages_under_review = TriageInteraction.objects.filter(review_status="under_review").count()
    
    # Data integrity verification (user satisfaction indicator)
    triages_verified = TriageInteraction.objects.filter(data_integrity_status="verified").count()
    triages_with_discrepancy = TriageInteraction.objects.filter(data_integrity_status="discrepancy").count()
    verification_rate = (triages_verified / total_triages * 100) if total_triages > 0 else 0
    
    # Note: Average review time calculation would require database-specific datetime arithmetic
    # For now, we'll skip this metric to keep it simple
    
    # Appointment Metrics
    total_appointments = Appointment.objects.count()
    appointments_this_month = Appointment.objects.filter(created_at__gte=month_ago_datetime).count()
    appointments_this_week = Appointment.objects.filter(created_at__gte=week_ago_datetime).count()
    appointments_today = Appointment.objects.filter(created_at__date=today).count()
    
    # Appointment status distribution
    appointment_status_dist = Appointment.objects.values('status').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Appointment completion rate (user satisfaction indicator)
    completed_appointments = Appointment.objects.filter(status="completed").count()
    appointment_completion_rate = (completed_appointments / total_appointments * 100) if total_appointments > 0 else 0
    
    # Appointment cancellation rate
    cancelled_appointments = Appointment.objects.filter(status="cancelled").count()
    cancellation_rate = (cancelled_appointments / total_appointments * 100) if total_appointments > 0 else 0
    
    # Doctor Metrics
    total_doctors_with_profiles = DoctorProfile.objects.count()
    doctors_with_availability = DoctorProfile.objects.filter(
        availabilities__is_available=True
    ).distinct().count()
    
    # Time-based trends (last 7 days)
    triage_trends = []
    appointment_trends = []
    for i in range(7):
        date = today - timedelta(days=6-i)
        triage_count = TriageInteraction.objects.filter(created_at__date=date).count()
        appointment_count = Appointment.objects.filter(created_at__date=date).count()
        triage_trends.append({
            'date': date.strftime('%Y-%m-%d'),
            'label': date.strftime('%b %d'),
            'count': triage_count
        })
        appointment_trends.append({
            'date': date.strftime('%Y-%m-%d'),
            'label': date.strftime('%b %d'),
            'count': appointment_count
        })
    
    # Average appointments per doctor
    if total_doctors_with_profiles > 0:
        avg_appointments_per_doctor = total_appointments / total_doctors_with_profiles
    else:
        avg_appointments_per_doctor = 0
    
    # User satisfaction score (composite metric)
    satisfaction_score = (
        onboarding_rate * 0.2 +
        triage_review_rate * 0.3 +
        verification_rate * 0.2 +
        appointment_completion_rate * 0.3
    )
    
    context = {
        # User Metrics
        'total_users': total_users,
        'total_patients': total_patients,
        'total_doctors': total_doctors,
        'active_users': active_users,
        'onboarding_completed': onboarding_completed,
        'onboarding_rate': round(onboarding_rate, 1),
        'new_users_month': new_users_month,
        'new_users_week': new_users_week,
        
        # Triage Metrics
        'total_triages': total_triages,
        'triages_this_month': triages_this_month,
        'triages_this_week': triages_this_week,
        'triages_today': triages_today,
        'severity_dist': list(severity_dist),
        'triages_reviewed': triages_reviewed,
        'triage_review_rate': round(triage_review_rate, 1),
        'triages_pending_review': triages_pending_review,
        'triages_under_review': triages_under_review,
        
        # Data Integrity
        'triages_verified': triages_verified,
        'triages_with_discrepancy': triages_with_discrepancy,
        'verification_rate': round(verification_rate, 1),
        
        # Appointment Metrics
        'total_appointments': total_appointments,
        'appointments_this_month': appointments_this_month,
        'appointments_this_week': appointments_this_week,
        'appointments_today': appointments_today,
        'appointment_status_dist': list(appointment_status_dist),
        'completed_appointments': completed_appointments,
        'appointment_completion_rate': round(appointment_completion_rate, 1),
        'cancelled_appointments': cancelled_appointments,
        'cancellation_rate': round(cancellation_rate, 1),
        
        # Doctor Metrics
        'total_doctors_with_profiles': total_doctors_with_profiles,
        'doctors_with_availability': doctors_with_availability,
        'avg_appointments_per_doctor': round(avg_appointments_per_doctor, 1),
        
        # Trends
        'triage_trends': triage_trends,
        'appointment_trends': appointment_trends,
        
        # Overall Satisfaction
        'satisfaction_score': round(satisfaction_score, 1),
        
        # Meta
        'last_updated': now,
    }
    
    return render(request, 'admin/dashboard.html', context)


@staff_member_required
def admin_dashboard_api(request):
    """API endpoint for AJAX updates of dashboard metrics."""
    now = timezone.now()
    today = now.date()
    week_ago = today - timedelta(days=7)
    week_ago_datetime = timezone.make_aware(datetime.combine(week_ago, datetime.min.time()))
    
    # Quick stats for real-time updates
    stats = {
        'triages_today': TriageInteraction.objects.filter(created_at__date=today).count(),
        'appointments_today': Appointment.objects.filter(created_at__date=today).count(),
        'triages_this_week': TriageInteraction.objects.filter(created_at__gte=week_ago_datetime).count(),
        'appointments_this_week': Appointment.objects.filter(created_at__gte=week_ago_datetime).count(),
        'last_updated': now.isoformat(),
    }
    
    return JsonResponse(stats)

