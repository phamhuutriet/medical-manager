from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from phonenumber_field.modelfields import PhoneNumberField
from .core.enums import *
import uuid


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

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=100)
    note = models.TextField(blank=True)
    allergies = models.TextField() # encoded list
    user = models.ForeignKey(MedicalUser, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now=True)


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
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    reason_for_visit = models.CharField(max_length=255)
    medical_history = models.TextField()  # encoded list of objects
    symptom = models.CharField(max_length=255)
    vital_signs = models.TextField()  # encoded list of objects
    diagnosis = models.CharField(max_length=255)
    treatment_plan = models.TextField()  # encoded list
    # template = models.ForeignKey(Template, on_delete=models.CASCADE, null=True)
    created_at = models.DateField(auto_now=True)
    

class Treatment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # template = models.ForeignKey(Template, on_delete=models.CASCADE)
    # data = models.TextField() # encoded object
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    date = models.DateField()
    name = models.CharField(max_length=255)
    cost = models.IntegerField(default=0)
    note = models.CharField(max_length=255)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

def upload_path(instance, filename):
    return '/'.join(['covers', str(instance.title), filename])

class Test(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    created_at = models.DateField() # Must be provided
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/")
