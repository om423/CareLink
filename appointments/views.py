from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from accounts.views import doctor_required, get_user_role, patient_required

from .forms import AppointmentBookingForm, AppointmentEditForm, AppointmentUpdateForm
from .models import Appointment


@patient_required
def index(request):
    """List all appointments for the current patient."""
    appointments = Appointment.objects.filter(patient=request.user).order_by(
        "-appointment_date", "-appointment_time"
    )
    # Annotate with can_be_edited for template
    upcoming_appointments = list(appointments.filter(status__in=["pending", "confirmed"]))
    for appointment in upcoming_appointments:
        appointment.can_be_edited = appointment.can_be_edited()
    
    context = {
        "appointments": appointments,
        "upcoming": upcoming_appointments,
        "past": appointments.filter(status__in=["completed", "cancelled"]),
    }
    return render(request, "appointments/my_appointments.html", context)


@patient_required
def book(request):
    """Book a new appointment or edit an existing one."""
    # Check if we're editing an existing appointment (for both GET and POST)
    edit_appointment_id = request.GET.get("edit") or request.POST.get("edit_appointment_id")
    edit_appointment = None
    if edit_appointment_id:
        try:
            edit_appointment = get_object_or_404(Appointment, id=edit_appointment_id, patient=request.user)
            if edit_appointment.status not in ["pending", "confirmed"]:
                messages.error(request, "This appointment cannot be edited.")
                edit_appointment = None
        except:
            edit_appointment = None
    
    if request.method == "POST":
        # Handle both form-based and AJAX-based submissions
        doctor_id = request.POST.get("doctor")
        appointment_date = request.POST.get("appointment_date")
        appointment_time = request.POST.get("appointment_time")
        appointment_type = request.POST.get("appointment_type", "in_person")
        reason = request.POST.get("reason", "")
        
        if doctor_id and appointment_date and appointment_time:
            try:
                from django.contrib.auth.models import User
                doctor = User.objects.get(id=doctor_id, patient_profile__role="doctor")
                
                # Convert time string to time object if needed
                from datetime import datetime
                if isinstance(appointment_time, str):
                    # Handle formats like "10:00 AM" or "10:00"
                    try:
                        appointment_time = appointment_time.strip()
                        if "AM" in appointment_time.upper() or "PM" in appointment_time.upper():
                            # Try different formats
                            for fmt in ["%I:%M %p", "%I:%M%p", "%I %p"]:
                                try:
                                    time_obj = datetime.strptime(appointment_time, fmt).time()
                                    appointment_time = time_obj
                                    break
                                except:
                                    continue
                        else:
                            # 24-hour format
                            time_obj = datetime.strptime(appointment_time, "%H:%M").time()
                            appointment_time = time_obj
                    except Exception as e:
                        messages.error(request, f"Invalid time format: {appointment_time}")
                        return redirect("appointments:book")
                
                # Update existing appointment or create new one
                if edit_appointment:
                    edit_appointment.doctor = doctor
                    edit_appointment.appointment_date = appointment_date
                    edit_appointment.appointment_time = appointment_time
                    edit_appointment.appointment_type = appointment_type
                    edit_appointment.reason = reason
                    edit_appointment.save()
                    appointment = edit_appointment
                    messages.success(
                        request,
                        f"Appointment updated successfully! "
                        f"Your appointment with {appointment.doctor.get_full_name() or appointment.doctor.username} is now scheduled for "
                        f"{appointment.appointment_date} at {appointment.appointment_time}.",
                    )
                else:
                    appointment = Appointment.objects.create(
                        patient=request.user,
                        doctor=doctor,
                        appointment_date=appointment_date,
                        appointment_time=appointment_time,
                        appointment_type=appointment_type,
                        reason=reason,
                        status="pending",
                    )
                    messages.success(
                        request,
                        f"Appointment booked successfully! "
                        f"Your appointment with {appointment.doctor.get_full_name() or appointment.doctor.username} is scheduled for "
                        f"{appointment.appointment_date} at {appointment.appointment_time}.",
                    )
                return redirect("appointments:detail", appointment_id=appointment.id)
            except User.DoesNotExist:
                messages.error(request, "Selected doctor not found.")
            except Exception as e:
                messages.error(request, f"Error booking appointment: {str(e)}")
        else:
            # Try form-based submission
            form = AppointmentBookingForm(request.POST)
            if form.is_valid():
                appointment = Appointment.objects.create(
                    patient=request.user,
                    doctor=form.cleaned_data["doctor"],
                    appointment_date=form.cleaned_data["appointment_date"],
                    appointment_time=form.cleaned_data["appointment_time"],
                    appointment_type=form.cleaned_data.get("appointment_type", "in_person"),
                    reason=form.cleaned_data.get("reason", ""),
                    status="pending",
                )
                messages.success(
                    request,
                    f"Appointment booked successfully! "
                    f"Your appointment with {appointment.doctor.username} is scheduled for "
                    f"{appointment.appointment_date} at {appointment.appointment_time}.",
                )
                return redirect("appointments:detail", appointment_id=appointment.id)

    # Get list of available doctors
    from django.contrib.auth.models import User

    doctors = User.objects.filter(patient_profile__role="doctor").order_by("username")
    
    # Extract specialty for each doctor and get all unique specialties
    doctors_with_specialty = []
    specialties_set = set()
    
    for doctor in doctors:
        specialty = "General Practice"
        if doctor.last_name and "(" in doctor.last_name:
            # Extract specialty from last_name like "Chen (Cardiologist)"
            try:
                start = doctor.last_name.find("(") + 1
                end = doctor.last_name.find(")")
                if start > 0 and end > start:
                    specialty = doctor.last_name[start:end]
            except:
                pass
        specialties_set.add(specialty)
        doctors_with_specialty.append({
            "doctor": doctor,
            "specialty": specialty,
        })
    
    # Get filter from query parameter
    selected_specialty = request.GET.get("specialty", "")
    
    # Filter doctors by specialty if filter is selected
    if selected_specialty:
        doctors_with_specialty = [
            item for item in doctors_with_specialty 
            if item["specialty"] == selected_specialty
        ]

    # Sort specialties alphabetically, but put "General Practice" first
    specialties_list = sorted(list(specialties_set))
    if "General Practice" in specialties_list:
        specialties_list.remove("General Practice")
        specialties = ["General Practice"] + sorted(specialties_list)
    else:
        specialties = specialties_list

    # Use the booking template (templates/appointments/index.html for the fancy UI)
    # This template is in the global templates directory and shows doctor cards
    context = {
        "doctors": doctors,
        "doctors_with_specialty": doctors_with_specialty,
        "specialties": specialties,
        "selected_specialty": selected_specialty,
        "edit_appointment": edit_appointment,
    }
    return render(request, "appointments/index.html", context)


@login_required
def detail(request, appointment_id):
    """View appointment details."""
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Check permissions: patient can view their own, doctor can view their appointments
    role = get_user_role(request.user)
    if role == "patient" and appointment.patient != request.user:
        messages.error(request, "You don't have permission to view this appointment.")
        return redirect("appointments:index")
    elif role == "doctor" and appointment.doctor != request.user:
        messages.error(request, "You don't have permission to view this appointment.")
        return redirect("doctors:index")

    # Doctor can update notes
    update_form = None
    if role == "doctor" and request.method == "POST":
        update_form = AppointmentUpdateForm(request.POST)
        if update_form.is_valid():
            appointment.notes = update_form.cleaned_data.get("notes", "")
            appointment.save()
            messages.success(request, "Appointment notes updated successfully.")
            return redirect("appointments:detail", appointment_id=appointment.id)
    else:
        update_form = AppointmentUpdateForm(initial={"notes": appointment.notes})

    context = {
        "appointment": appointment,
        "update_form": update_form,
        "is_doctor": role == "doctor",
        "can_cancel": appointment.can_be_cancelled(),
        "can_edit": role == "patient" and appointment.can_be_edited(),
    }
    return render(request, "appointments/detail.html", context)


@patient_required
def edit(request, appointment_id):
    """Edit an existing appointment - redirects to booking page with appointment ID."""
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)

    # Check if appointment can be edited (status check)
    if appointment.status not in ["pending", "confirmed"]:
        messages.error(
            request,
            "This appointment cannot be edited. "
            "It may have been completed or cancelled.",
        )
        return redirect("appointments:detail", appointment_id=appointment.id)

    # Redirect to booking page with appointment ID for editing
    return redirect(f"{reverse('appointments:book')}?edit={appointment_id}")


@login_required
@require_POST
def cancel(request, appointment_id):
    """Cancel an appointment."""
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Check permissions
    role = get_user_role(request.user)
    if role == "patient" and appointment.patient != request.user:
        messages.error(request, "You don't have permission to cancel this appointment.")
        return redirect("appointments:index")
    elif role == "doctor" and appointment.doctor != request.user:
        messages.error(request, "You don't have permission to cancel this appointment.")
        return redirect("doctors:index")

    if not appointment.can_be_cancelled():
        messages.error(
            request,
            "This appointment cannot be cancelled. "
            "It may have already passed or been completed.",
        )
        return redirect("appointments:detail", appointment_id=appointment.id)

    appointment.status = "cancelled"
    appointment.save()
    messages.success(request, "Appointment cancelled successfully.")
    return redirect("appointments:detail", appointment_id=appointment.id)


@doctor_required
def doctor_appointments(request):
    """List all appointments for the current doctor."""
    appointments = Appointment.objects.filter(doctor=request.user).order_by(
        "-appointment_date", "-appointment_time"
    )
    context = {
        "appointments": appointments,
        "upcoming": appointments.filter(status__in=["pending", "confirmed"]),
        "past": appointments.filter(status__in=["completed", "cancelled"]),
    }
    return render(request, "appointments/doctor_appointments.html", context)


@doctor_required
@require_POST
def confirm(request, appointment_id):
    """Doctor confirms an appointment."""
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user)

    if appointment.status != "pending":
        messages.error(
            request, "Only pending appointments can be confirmed."
        )
        return redirect("appointments:detail", appointment_id=appointment.id)

    appointment.status = "confirmed"
    appointment.save()
    messages.success(request, "Appointment confirmed successfully.")
    return redirect("appointments:detail", appointment_id=appointment.id)


@doctor_required
@require_POST
def complete(request, appointment_id):
    """Doctor marks an appointment as completed."""
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user)

    if appointment.status not in ["pending", "confirmed"]:
        messages.error(
            request, "Only pending or confirmed appointments can be completed."
        )
        return redirect("appointments:detail", appointment_id=appointment.id)

    appointment.status = "completed"
    appointment.save()
    messages.success(request, "Appointment marked as completed.")
    return redirect("appointments:detail", appointment_id=appointment.id)
