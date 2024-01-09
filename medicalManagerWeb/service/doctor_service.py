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
        return BadRequestErrorResponse(message="Role not found")
    
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

    return SuccessResponse(message="Doctor created", metadata=format_doctor(doctor))


def update_doctor(request_data, uid, did):
    try:
        name = request_data["name"]
        phone_number = request_data["phoneNumber"]
        role_id = request_data["role"]["id"]
    except KeyError as e:
        return BadRequestErrorResponse(message="Key error: " + str(e))
    
    try:
        role = Role.objects.get(pk=role_id)
    except ObjectDoesNotExist:
        return BadRequestErrorResponse(message="Role not found")
    
    user = MedicalUser.objects.get(pk=uid)

    try: 
        doctor = Doctor.objects.get(pk=did)

        if doctor.user != user:
            return BadRequestErrorResponse(message="You don't have permission to update this doctor")

        doctor.name = name
        doctor.phone_number = phone_number
        doctor.role = role
        doctor.save()
    except ObjectDoesNotExist:
        return BadRequestErrorResponse(message="Doctor not found")
    
    return SuccessResponse(message="Doctor updated", metadata=format_doctor(doctor))


def get_single_doctor(uid, doctor_id: str):
    try:
        doctor = Doctor.objects.get(pk=doctor_id)
    except ObjectDoesNotExist:
        return BadRequestErrorResponse(message="Doctor not found")
    
    user = MedicalUser.objects.get(pk=uid)
    if doctor.user != user:
        return BadRequestErrorResponse(message="You don't have permission to view this user")
    
    return OKResponse(message="Get doctor successfully", metadata=format_doctor(doctor))


def get_all_doctors(uid):
    user = MedicalUser.objects.get(pk=uid)
    doctors = list(Doctor.objects.all().filter(user=user))
    formatted_doctors = [format_doctor(doctor) for doctor in doctors]

    return OKResponse(message="Get all doctors", metadata=formatted_doctors)