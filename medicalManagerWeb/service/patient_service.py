from ..core.error_response import *
from ..core.success_response import *
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from ..models import *
from ..utils.formatter import *
import json


def is_user_patient(user: MedicalUser, patient: Patient):
    user_patients = Patient.objects.all().filter(user=user)
    return patient in user_patients


def create_patient(request_data, uid):
    try:
        name = request_data["name"]
        gender = request_data["gender"]
        date_of_birth = request_data["dateOfBirth"]
        address = request_data["address"]
        phone_number = request_data["phoneNumber"]
        note = request_data["note"]
        allergies = request_data["allergies"]
    except KeyError as e:
        return BadRequestErrorResponse(message="Key error: " + str(e))
    
    user = MedicalUser.objects.get(pk=uid)

    try: 
        patient = Patient()
        patient.name = name
        patient.gender = gender
        patient.date_of_birth = date_of_birth
        patient.address = address
        patient.phone_number = phone_number
        patient.note = note
        patient.allergies = json.dumps(allergies)
        patient.user = user
        patient.save()
    except Exception as e:
        return BadRequestErrorResponse(message="Error saving patient: " + str(e))
    
    return SuccessResponse(message="Patient created", metadata=format_patient(patient))


def get_patient(pid, uid):
    try:
        patient = Patient.objects.get(pk=pid)
    except ObjectDoesNotExist:
        return BadRequestErrorResponse(message="Patient not found")
    
    user = MedicalUser.objects.get(pk=uid)
    if not is_user_patient(user, patient):
        return BadRequestErrorResponse(message="You don't have permission to view this patient")
    
    return OKResponse(message="Get patient successfully", metadata=format_patient(patient))


def get_all_patients(uid):
    # TODO: filter by doctor and date -> must have record model first
    user = MedicalUser.objects.get(pk=uid)
    patients = list(Patient.objects.all().filter(user=user))
    formatted_patients = [format_patient(patient) for patient in patients]

    return OKResponse(message="Get all patient successfully", metadata=formatted_patients)


def update_patients(request_data, pid, uid):
    try:
        patient = Patient.objects.get(pk=pid)
    except ObjectDoesNotExist:
        return BadRequestErrorResponse(message="Patient not found")
    
    user = MedicalUser.objects.get(pk=uid)
    if not is_user_patient(user, patient):
        return BadRequestErrorResponse(message="You don't have permission to update this patient")
    
    try:
        name = request_data["name"]
        gender = request_data["gender"]
        date_of_birth = request_data["dateOfBirth"]
        address = request_data["address"]
        phone_number = request_data["phoneNumber"]
        note = request_data["note"]
        allergies = request_data["allergies"]
    except KeyError as e:
        return BadRequestErrorResponse(message="Key error: " + str(e))
    
    try:
        patient.name = name
        patient.gender = gender
        patient.date_of_birth = date_of_birth
        patient.address = address
        patient.phone_number = phone_number
        patient.note = note
        patient.allergies = json.dumps(allergies)
        patient.save()
    except Exception as e:
        return BadRequestErrorResponse(message="Error updateing patient " + str(e))
    
    return SuccessResponse(message="Update patient successfully", metadata=format_patient(patient))