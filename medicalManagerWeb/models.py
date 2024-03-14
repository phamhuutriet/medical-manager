import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from phonenumber_field.modelfields import PhoneNumberField
from .core.enums import *


class MedicalUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)


class UserSignUpRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    approved = models.BooleanField(default=False)
    email = models.EmailField(unique=True)


class KeyToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(MedicalUser, on_delete=models.CASCADE)
    public_key = models.CharField(max_length=1000, null=True)
    refresh_token = models.CharField(max_length=1000, null=True)


class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    user = models.ForeignKey(MedicalUser, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['user', 'name']]


class Doctor(models.Model):
    GENDER_CHOICES = [
        (GENDER.M.value, 'Male'),
        (GENDER.F.value, 'Female'),
        (GENDER.O.value, 'Other'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    phone_number = PhoneNumberField()   
    user = models.ForeignKey(MedicalUser, on_delete=models.CASCADE)
    date_of_birth = models.DateField()

    class Meta:
        unique_together = [['user', 'first_name', 'last_name']]


class Patient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    GENDER_CHOICES = [
        (GENDER.M.value, 'Male'),
        (GENDER.F.value, 'Female'),
        (GENDER.O.value, 'Other'),
    ]

    name = models.CharField(max_length=100, unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=255)
    phone_number = PhoneNumberField()
    note = models.TextField(blank=True)
    allergies = models.TextField() # encoded list
    user = models.ForeignKey(MedicalUser, on_delete=models.CASCADE)
    


class Template(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
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

    class Meta:
        unique_together = [['user', 'name']]


class Record(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
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


class Treatment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    data = models.TextField() # encoded object

    