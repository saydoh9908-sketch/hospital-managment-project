# main/admin.py

from django.contrib import admin
from .models import Patient, Doctor, Appointment # Import your models

# Register your models here.
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Appointment)