from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES)
    phone = models.CharField(max_length=20)
    #email = models.EmailField(unique=True, null=False, blank=False)


    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    # This line MUST be commented out or deleted
    #email = models.EmailField(unique=True, null=False , blank=False)

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}"

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    reason = models.TextField()

    def __str__(self):
        return f"Appointment with {self.doctor} for {self.patient}"