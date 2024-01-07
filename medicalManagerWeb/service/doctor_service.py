from ..core.error_response import *
from ..core.success_response import *
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from ..models import *
from ..utils.formatter import *


def create_doctor(request_data):
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
    
    try:
        doctor = Doctor()
        doctor.name = name
        doctor.phone_number = phone_number
        doctor.role = role 
        doctor.save()
    except IntegrityError:
        return BadRequestErrorResponse(message="Doctor name is already existed")

    return OKResponse(message="Doctor created")


def get_single_doctor(doctor_id: str):
    try:
        doctor = Doctor.objects.get(pk=doctor_id)
    except ObjectDoesNotExist:
        return BadRequestErrorResponse(message="Doctor not found")
    
    return OKResponse(message="Get doctor successfully", metadata=format_doctor(doctor))
