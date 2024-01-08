from ..core.error_response import *
from ..core.success_response import *
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from ..models import *
from ..utils.formatter import *
import json


def create_record(request_data):
    try:
        patient_id = request_data["patient"]["id"]
        reason_for_visit = request_data["reasonForVisit"]
        symptom = request_data["symptom"]
        medical_history = request_data["medicalHistory"]
        vital_signs = request_data["vitalSigns"]
        observation = request_data["observations"]
        diagnosis = request_data["diagnosis"]
        primary_doctor_id = request_data["doctor"]["id"]
        treatment_plan = request_data["treatmentPlan"]
    except KeyError as e:
        return BadRequestErrorResponse(message="Key error: " + str(e))
    
    
    try:
        patient = Patient.objects.get(pk=patient_id)
    except ObjectDoesNotExist:
        return BadRequestErrorResponse(message="Patient not found")
    
    try:
        primary_doctor = Doctor.objects.get(pk=primary_doctor_id)
    except ObjectDoesNotExist:
        return BadRequestErrorResponse(message="Doctor not found")
    
    try:
        record = Record()
        record.patient = patient
        record.reason_for_visit = reason_for_visit
        record.symptom = symptom
        record.medical_history = json.dumps(medical_history)
        record.vital_signs = json.dumps(vital_signs)
        record.observation = json.dumps(observation)
        record.diagnosis = diagnosis
        record.primary_doctor = primary_doctor
        record.treatment_plan = json.dumps(treatment_plan)
        record.save()
    except Exception as e:
        return BadRequestErrorResponse(message="Error saving record " + str(e))
    
    return SuccessResponse(message="Record created", metadata=format_record(record))