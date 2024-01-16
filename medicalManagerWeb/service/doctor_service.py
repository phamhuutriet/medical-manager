from ..core.error_response import *
from ..core.success_response import *
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from ..models import *
from ..core.serializers import *


def create_doctor(request_data, uid):
    serializer = DoctorSerializer(data=request_data)
    serializer.is_valid(raise_exception=True)
    user = MedicalUser.objects.get(pk=uid)

    try:
        doctor = serializer.save(user=user)
    except IntegrityError as e:
        return BadRequestErrorResponse(message="Error saving doctor: " + str(e))
    
    doctor_serializer = DoctorSerializer(doctor)
    return CreatedResponse(message="Doctor created", metadata=doctor_serializer.data)


def update_doctor(request_data, did):
    doctor = Doctor.objects.get(pk=did)
    serializer = DoctorSerializer(doctor, data=request_data)
    serializer.is_valid(raise_exception=True)

    try:
        updated_doctor = serializer.save()
    except IntegrityError as e:
        return BadRequestErrorResponse(message="Error saving doctor: " + str(e))
        
    doctor_serializer = DoctorSerializer(updated_doctor)
    return CreatedResponse(message="Doctor updated", metadata=doctor_serializer.data)


def get_single_doctor(did: str):
    doctor = Doctor.objects.get(pk=did)
    doctor_serializer = DoctorSerializer(doctor)
    return OKResponse(message="Get doctor successfully", metadata=doctor_serializer.data)


def get_all_doctors(uid):
    user = MedicalUser.objects.get(pk=uid)
    doctors = list(Doctor.objects.all().filter(user=user))
    serialized_doctors = [DoctorSerializer(doctor).data for doctor in doctors]
    return OKResponse(message="Get all doctors", metadata=serialized_doctors)


def doctor_authenticate(uid, did, callback):
    user = MedicalUser.objects.get(pk=uid)
    
    try:
        doctor = Doctor.objects.get(pk=did)
    except ObjectDoesNotExist:
        return NotFoundErrorResponse(message="Doctor not found")
    
    if doctor.user != user:
        return BadRequestErrorResponse(message="You don't have the permission to access this doctor")
    
    return callback()
