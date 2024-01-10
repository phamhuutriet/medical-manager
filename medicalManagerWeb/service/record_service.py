from ..core.error_response import *
from ..core.success_response import *
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import OuterRef, Subquery
from ..models import *
from ..utils.formatter import *
from ..core.template_validator import *
import json


def create_record(request_data, pid, uid):
    try:
        reason_for_visit = request_data["reasonForVisit"]
        symptom = request_data["symptom"]
        medical_history = request_data["medicalHistory"]
        vital_signs = request_data["vitalSigns"]
        observation = request_data["observations"]
        diagnosis = request_data["diagnosis"]
        primary_doctor_id = request_data["doctor"]["id"]
        treatment_plan = request_data["treatmentPlan"]
        template_id = request_data["template"]["id"]
    except KeyError as e:
        return BadRequestErrorResponse(message="Key error: " + str(e))
    
    patient = Patient.objects.get(pk=pid)
    user = MedicalUser.objects.get(pk=uid)
    
    try:
        primary_doctor = Doctor.objects.get(pk=primary_doctor_id)
        if primary_doctor.user != user:
            return BadRequestErrorResponse(message="You don't have the permission to access this doctor")
    except ObjectDoesNotExist:
        return NotFoundErrorResponse(message="Doctor not found")
    
    try:
        template = Template.objects.get(pk=template_id)
        if template.user != user:
            return BadRequestErrorResponse(message="You don't have the permission to access this template")
    except ObjectDoesNotExist:
        return NotFoundErrorResponse(message="Template not found")
    
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
        record.template = template

        # Validate template first
        if not validate_record_template(record, template):
            return BadRequestErrorResponse(message="Template and record are not matched")

        record.save()
    except Exception as e:
        return BadRequestErrorResponse(message="Error saving record " + str(e))
    
    return CreatedResponse(message="Record created", metadata=format_record(record))


def get_record(rid, query_params):
    version = None
    if "version" in query_params:
        version = query_params["version"]
        if not version.isdigit():
            return BadRequestErrorResponse(message="TypeError: version must be integer")

    try:
        if version is None:
            # If version is None, get the latest version of the record
            record = Record.objects.filter(record_id=rid).order_by('-version').first()
        else:
            # If version is provided, get the specific version of the record
            record = Record.objects.get(record_id=rid, version=version)
    except ObjectDoesNotExist:
        return BadRequestErrorResponse(message="Record not found")
    
    # Validate template first
    if not validate_record_template(record, record.template):
        return BadRequestErrorResponse(message="Template and record are not matched")
        
    return OKResponse(message="Get record successfully", metadata=format_record(record))


def update_record(request_data, pid, rid, uid):
    try:
        reason_for_visit = request_data["reasonForVisit"]
        symptom = request_data["symptom"]
        medical_history = request_data["medicalHistory"]
        vital_signs = request_data["vitalSigns"]
        observation = request_data["observations"]
        diagnosis = request_data["diagnosis"]
        primary_doctor_id = request_data["doctor"]["id"]
        treatment_plan = request_data["treatmentPlan"]
        template_id = request_data["template"]["id"]
    except KeyError as e:
        return BadRequestErrorResponse(message="Key error: " + str(e))
    
    patient = Patient.objects.get(pk=pid)
    user = MedicalUser.objects.get(pk=uid)

    try:
        primary_doctor = Doctor.objects.get(pk=primary_doctor_id)
        if primary_doctor.user != user:
            return BadRequestErrorResponse(message="You don't have the permission to access this doctor")
    except ObjectDoesNotExist:
        return NotFoundErrorResponse(message="Doctor not found")
    
    try:
        template = Template.objects.get(pk=template_id)
        if template.user != user:
            return BadRequestErrorResponse(message="You don't have the permission to access this template")
    except ObjectDoesNotExist:
        return NotFoundErrorResponse(message="Template not found")
    
    try:
        # Create new version of old record -> immutable data
        record = Record()
        # Define record by record id
        record.record_id = rid
        record.patient = patient
        record.reason_for_visit = reason_for_visit
        record.symptom = symptom
        record.medical_history = json.dumps(medical_history)
        record.vital_signs = json.dumps(vital_signs)
        record.observation = json.dumps(observation)
        record.diagnosis = diagnosis
        record.primary_doctor = primary_doctor
        record.treatment_plan = json.dumps(treatment_plan)
        record.template = template

        # Validate template first
        if not validate_record_template(record, template):
            return BadRequestErrorResponse(message="Template and record are not matched")

        record.save()
    except Exception as e:
        return BadRequestErrorResponse(message="Error saving record " + str(e))
    
    return CreatedResponse(message="Record updated", metadata=format_record(record))


def get_all_records(pid):
    patient = Patient.objects.get(pk=pid)
    # Find the latest version for each record_id
    latest_versions = Record.objects.filter(
        patient=patient,
        record_id=OuterRef('record_id')
    ).order_by('-version').values('version')[:1]

    # Query to get only the records that match the latest version for each record_id
    patient_records = Record.objects.filter(
        patient=patient,
        version=Subquery(latest_versions)
    )

    formatted_patient_records = [format_record(record) for record in patient_records]

    return OKResponse(message="Get all records from patient", metadata=formatted_patient_records)


def record_authenticate(pid, rid, callback):
    patient = Patient.objects.get(pk=pid)

    try:
        record = Record.objects.filter(
            record_id=rid
        ).order_by('-version')[:1].get()
    except ObjectDoesNotExist:
        return NotFoundErrorResponse(message="Record not found")
    
    if record.patient != patient:
        return BadRequestErrorResponse(message="You don't have the permission to access this record")
    
    return callback()