import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from phonenumber_field.modelfields import PhoneNumberField
from .core.enums import *


class MedicalUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    display_name = models.CharField(max_length=255, unique=True)
    
    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)


class UserSignUpRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    display_name = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    approved = models.BooleanField(default=False)
    email = models.EmailField()


class KeyToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(MedicalUser, on_delete=models.CASCADE)
    public_key = models.CharField(max_length=1000, null=True)
    refresh_token = models.CharField(max_length=1000, null=True)


class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(MedicalUser, on_delete=models.CASCADE)


class Doctor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    phone_number = PhoneNumberField()   
    user = models.ForeignKey(MedicalUser, on_delete=models.CASCADE)


class Patient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    GENDER_CHOICES = [
        (GENDER.M, 'Male'),
        (GENDER.F, 'Female'),
        (GENDER.O, 'Other'),
    ]

    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=255)
    phone_number = PhoneNumberField()
    note = models.TextField(blank=True)
    allergies = models.TextField() # encoded list
    user = models.ForeignKey(MedicalUser, on_delete=models.CASCADE)


class Template(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    # encoded object
    # object format: {<column_name> : <column_type>} -> must have enum?
    medical_history_columns = models.TextField()  
    # encoded object
    # object format: {<column_name> : <column_type>} -> must have enum?
    observation_columns = models.TextField()
    # encoded object
    # object format: {<column_name> : <column_type>} -> must have enum?
    treatment_columns = models.TextField()
    user = models.ForeignKey(MedicalUser, on_delete=models.CASCADE)


class Record(models.Model):
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    record_id = models.UUIDField(default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    reason_for_visit = models.CharField(max_length=255)
    symptom = models.CharField(max_length=255)
    medical_history = models.TextField()  # encoded list of objects
    vital_signs = models.TextField()  # encoded list of objects
    date = models.DateField(auto_now=True)
    observation = models.TextField(blank=True)
    diagnosis = models.CharField(max_length=255)
    primary_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    treatment_plan = models.TextField()  # encoded list
    version = models.IntegerField(editable=False)

    class Meta:
        unique_together = [['record_id', 'version']]

    def save(self, *args, **kwargs):
        if not self.version:
            # Retrieve the latest version of the current record and increment it by 1
            latest_version = Record.objects.filter(id=self.id).order_by('-version').first()
            self.version = (latest_version.version if latest_version else 0) + 1
        super(Record, self).save(*args, **kwargs)