from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from .models import Patient, Doctor, Appointment

class PatientRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}), label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}), label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose a username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email address'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Validate email format
            validator = EmailValidator(message="Please enter a valid email address")
            try:
                validator(email)
            except ValidationError:
                raise forms.ValidationError("Invalid email format. Please enter a valid email address (e.g., user@example.com)")
            
            # Check if email already exists
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("This email address is already registered")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

class DoctorRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}), label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}), label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose a username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email address'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Validate email format
            validator = EmailValidator(message="Please enter a valid email address")
            try:
                validator(email)
            except ValidationError:
                raise forms.ValidationError("Invalid email format. Please enter a valid email address (e.g., user@example.com)")
            
            # Check if email already exists
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("This email address is already registered")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

# --- Define choices for dropdowns ---
BLOOD_TYPE_CHOICES = [
    ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
    ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-'),
]

SPECIALIZATION_CHOICES = [
    ('Cardiology', 'Cardiology'), ('Dermatology', 'Dermatology'), ('Endocrinology', 'Endocrinology'),
    ('Gastroenterology', 'Gastroenterology'), ('General Practice', 'General Practice'), ('Neurology', 'Neurology'),
    ('Oncology', 'Oncology'), ('Pediatrics', 'Pediatrics'), ('Psychiatry', 'Psychiatry'),
    ('Radiology', 'Radiology'), ('Surgery', 'Surgery'), ('Urology', 'Urology'),
]

class PatientProfileForm(forms.ModelForm):
    blood_type = forms.ChoiceField(choices=BLOOD_TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    class Meta:
        model = Patient
        fields = ['date_of_birth', 'blood_type', 'phone']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
        }

class DoctorProfileForm(forms.ModelForm):
    specialization = forms.ChoiceField(choices=SPECIALIZATION_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    class Meta:
        model = Doctor
        fields = ['specialization', 'phone']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
        }

class AppointmentForm(forms.ModelForm):
    appointment_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), label="Appointment Date")
    appointment_time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}), label="Appointment Time")

    class Meta:
        model = Appointment
        exclude = ['patient']
        widgets = {
            # --- WIDGETS NOW HAVE CSS CLASSES DEFINED ---
            'doctor': forms.Select(attrs={'class': 'form-select'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Reason for visit...'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('appointment_date')
        time = cleaned_data.get('appointment_time')
        if date and time:
            from datetime import datetime
            combined_datetime = datetime.combine(date, time)
            cleaned_data['appointment_date'] = combined_datetime
        elif date and not time:
            raise forms.ValidationError("Please select a time for the appointment.")
        elif time and not date:
            raise forms.ValidationError("Please select a date for the appointment.")
        return cleaned_data
