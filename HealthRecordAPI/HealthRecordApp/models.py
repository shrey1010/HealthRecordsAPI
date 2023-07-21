# api/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser


class Department(models.Model):
    name = models.CharField(max_length=100)
    diagnostics = models.TextField()
    location = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)


class CustomUser(AbstractUser):
    pass


class Patient(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, primary_key=True)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, related_name='patients')


class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,
                                primary_key=True, default=None)  # Add default value
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, related_name='doctors')


class PatientRecord(models.Model):
    record_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    diagnostics = models.TextField()
    observations = models.TextField()
    treatments = models.TextField()
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True)
    misc = models.TextField()
