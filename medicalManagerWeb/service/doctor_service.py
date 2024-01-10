from ..core.error_response import *
from ..core.success_response import *
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from ..models import *
from ..utils.formatter import *


def create_doctor(request_data, uid):
    try:
        name = request_data["name"]
        phone_number = request_data["phoneNumber"]
        role_id = request_data["role"]["id"]
    except KeyError as e:
        return BadRequestErrorResponse(message="Key error: " + str(e))
    
    try:
        role = Role.objects.get(pk=role_id)
    except ObjectDoesNotExist:
        return NotFoundErrorResponse(message="Role not found")
    
    user = MedicalUser.objects.get(pk=uid)
    
    try:
        doctor = Doctor()
        doctor.name = name
        doctor.phone_number = phone_number
        doctor.role = role 
        doctor.user = user
        doctor.save()
    except IntegrityError:
        return BadRequestErrorResponse(message="Doctor name is already existed")

    return CreatedResponse(message="Doctor created", metadata=format_doctor(doctor))


def update_doctor(request_data, did):
    try:
        name = request_data["name"]
        phone_number = request_data["phoneNumber"]
        role_id = request_data["role"]["id"]
    except KeyError as e:
        return BadRequestErrorResponse(message="Key error: " + str(e))
    
    try:
        role = Role.objects.get(pk=role_id)
    except ObjectDoesNotExist:
        return NotFoundErrorResponse(message="Role not found")
    
    doctor = Doctor.objects.get(pk=did)
    doctor.name = name
    doctor.phone_number = phone_number
    doctor.role = role
    doctor.save()
    
    return CreatedResponse(message="Doctor updated", metadata=format_doctor(doctor))


def get_single_doctor(did: str):
    doctor = Doctor.objects.get(pk=did)
    return OKResponse(message="Get doctor successfully", metadata=format_doctor(doctor))


def get_all_doctors(uid):
    user = MedicalUser.objects.get(pk=uid)
    doctors = list(Doctor.objects.all().filter(user=user))
    formatted_doctors = [format_doctor(doctor) for doctor in doctors]

    return OKResponse(message="Get all doctors", metadata=formatted_doctors)


def doctor_authenticate(uid, did, callback):
    user = MedicalUser.objects.get(pk=uid)
    
    try:
        doctor = Doctor.objects.get(pk=did)
    except ObjectDoesNotExist:
        return NotFoundErrorResponse(message="Doctor not found")
    
    if doctor.user != user:
        return BadRequestErrorResponse(message="You don't have the permission to access this doctor")
    
    return callback()
