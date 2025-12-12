from tkinter import messagebox
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Patient, Doctor, Appointment
from .forms import (
    AppointmentForm,
    PatientRegistrationForm, DoctorRegistrationForm,
    PatientProfileForm, DoctorProfileForm
)

def home(request):
    return render(request, 'main/home.html')

class CustomLoginView(LoginView):
    template_name = 'main/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')

class CustomLogoutView(LogoutView):
    def get_success_url(self):
        return reverse_lazy('home')

def patient_register(request):
    if request.method == 'POST':
        user_form = PatientRegistrationForm(request.POST)
        profile_form = PatientProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            patient = profile_form.save(commit=False)
            patient.user = user
            patient.save()
            login(request, user) 
            return redirect('home')
        else:
            print("PATIENT REGISTRATION FAILED VALIDATION")
            print("User form errors:", user_form.errors)
            print("Profile form errors:", profile_form.errors)
            messagebox.showinfo("Alert Title", "This is the alert message!")
    else:
        user_form = PatientRegistrationForm()
        profile_form = PatientProfileForm()
    return render(request, 'main/patient_register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def doctor_register(request):
    if request.method == 'POST':
        user_form = DoctorRegistrationForm(request.POST)
        profile_form = DoctorProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            doctor = profile_form.save(commit=False)
            doctor.user = user
            doctor.save()
            login(request, user)
            return redirect('home')
    else:
        user_form = DoctorRegistrationForm()
        profile_form = DoctorProfileForm()
    return render(request, 'main/doctor_register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def patient_list(request):
    query = request.GET.get('q')
    if query:
        patients = Patient.objects.filter(
            Q(user__first_name__icontains=query) | 
            Q(user__last_name__icontains=query) | 
            Q(blood_type__icontains=query)
        )
    else:
        patients = Patient.objects.all()
    
    context = {'patients': patients}
    return render(request, 'main/patient_list.html', context)

def doctor_list(request):
    query = request.GET.get('q')
    if query:
        doctors = Doctor.objects.filter(
            Q(user__first_name__icontains=query) | 
            Q(user__last_name__icontains=query) | 
            Q(specialization__icontains=query)
        )
    else:
        doctors = Doctor.objects.all()
    
    context = {'doctors': doctors}
    return render(request, 'main/doctor_list.html', context)

def appointment_list(request):
    is_patient = hasattr(request.user, 'patient')
    is_doctor = hasattr(request.user, 'doctor')

    if is_patient:
        appointments = Appointment.objects.filter(patient=request.user.patient).order_by('appointment_date')
    elif is_doctor:
        appointments = Appointment.objects.filter(doctor=request.user.doctor).order_by('appointment_date')
    else:
        appointments = Appointment.objects.all().order_by('appointment_date')

    context = {
        'appointments': appointments,
        'is_patient': is_patient,
        'is_doctor': is_doctor
    }
    return render(request, 'main/appointment_list.html', context)

@login_required
def add_appointment(request):
    try:
        current_patient = request.user.patient
    except Patient.DoesNotExist:
        return redirect('home')

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            new_appointment = form.save(commit=False)
            new_appointment.patient = current_patient
            new_appointment.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm()

    context = {'form': form}
    return render(request, 'main/appointment_form.html', context)

@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.user.patient != appointment.patient:
        messages.error(request, "You cannot cancel an appointment that is not yours.")
        return redirect('appointment_list')

    appointment.delete()
    messages.success(request, "Your appointment has been successfully cancelled.")
    return redirect('appointment_list')

# --- NEW VIEW FOR EDITING AN APPOINTMENT ---
@login_required
def edit_appointment(request, appointment_id):
    # Get the appointment object or return a 404 error if not found
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # --- SECURITY CHECK: Ensure the logged-in user is the patient of the appointment ---
    if request.user.patient != appointment.patient:
        messages.error(request, "You cannot edit an appointment that is not yours.")
        return redirect('appointment_list')

    if request.method == 'POST':
        # Pass the instance to the form so it knows which appointment to update
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, "Your appointment has been successfully updated.")
            return redirect('appointment_list')
    else:
        # For GET requests, pre-populate the form with the appointment's data
        form = AppointmentForm(instance=appointment)

    context = {
        'form': form,
        'appointment': appointment # Pass the appointment object to the template
    }
    return render(request, 'main/edit_appointment.html', context)
