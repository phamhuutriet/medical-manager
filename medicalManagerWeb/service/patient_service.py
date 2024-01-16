from ..core.error_response import *
from ..core.success_response import *
from django.core.exceptions import ObjectDoesNotExist
from ..models import *
from ..utils.formatter import *
from ..core.serializers import *


def create_patient(request_data, uid):
    serializer = PatientSerializer(data=request_data)
    serializer.is_valid(raise_exception=True)
    user = MedicalUser.objects.get(pk=uid)

    try: 
        patient = serializer.save(user=user)
    except Exception as e:
        return BadRequestErrorResponse(message="Error saving patient: " + str(e))
    
    patient_serializer = PatientSerializer(patient)
    return CreatedResponse(message="Patient created", metadata=patient_serializer.data)


def get_patient(pid):
    patient = Patient.objects.get(pk=pid)
    patient_serializer = PatientSerializer(patient)
    return OKResponse(message="Get patient successfully", metadata=patient_serializer.data)


def get_all_patients(uid):
    # TODO: filter by doctor and date -> must have record model first
    user = MedicalUser.objects.get(pk=uid)
    patients = list(Patient.objects.all().filter(user=user))
    formatted_patients = [PatientSerializer(patient).data for patient in patients]

    return OKResponse(message="Get all patient successfully", metadata=formatted_patients)


def update_patients(request_data, pid):
    patient = Patient.objects.get(pk=pid)
    serializer = PatientSerializer(patient, data=request_data)
    serializer.is_valid(raise_exception=True)

    try: 
        patient = serializer.save()
    except Exception as e:
        return BadRequestErrorResponse(message="Error saving patient: " + str(e))
    
    patient_serializer = PatientSerializer(patient)
    return CreatedResponse(message="Patient updated", metadata=patient_serializer.data)


def patient_authenticate(uid, pid, callback):
    user = MedicalUser.objects.get(pk=uid)

    try:
        patient = Patient.objects.get(pk=pid)
    except ObjectDoesNotExist:
        return NotFoundErrorResponse(message="Patient not found")

    if patient.user != user:
        return BadRequestErrorResponse(message="You don't have permission to view this patient")
    
    return callback()