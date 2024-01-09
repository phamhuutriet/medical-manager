from ..core.error_response import *
from ..core.success_response import *
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import OuterRef, Subquery
from ..models import *
from ..utils.formatter import *
from ..core.template_validator import *
import json


def is_patient_record(patient: Patient, record: Record):
    patient_records = Record.objects.all().filter(patient=patient)
    return record in patient_records


def create_record(request_data, pid):
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
    
    try:
        patient = Patient.objects.get(pk=pid)
    except ObjectDoesNotExist:
        return BadRequestErrorResponse(message="Patient not found")
    
    try:
        primary_doctor = Doctor.objects.get(pk=primary_doctor_id)
    except ObjectDoesNotExist:
        return BadRequestErrorResponse(message="Doctor not found")
    
    try:
        template = Template.objects.get(pk=template_id)
    except ObjectDoesNotExist:
        return BadRequestErrorResponse(message="Template not found")
    
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
    
    return SuccessResponse(message="Record created", metadata=format_record(record))


def get_record(pid, rid, query_params):
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
    
    patient = Patient.objects.get(pk=pid)

    # Validate template first
    if not validate_record_template(record, record.template):
        return BadRequestErrorResponse(message="Template and record are not matched")

    if not is_patient_record(patient, record):
        return BadRequestErrorResponse(message="You don't have permission to view this record")
        
    return OKResponse(message="Get record successfully", metadata=format_record(record))


def update_record(request_data, pid, rid):
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
    
    try:
        patient = Patient.objects.get(pk=pid)
    except ObjectDoesNotExist:
        return BadRequestErrorResponse(message="Patient not found")
    
    try:
        primary_doctor = Doctor.objects.get(pk=primary_doctor_id)
    except ObjectDoesNotExist:
        return BadRequestErrorResponse(message="Doctor not found")
    
    try:
        template = Template.objects.get(pk=template_id)
    except ObjectDoesNotExist:
        return BadRequestErrorResponse(message="Template not found")
    
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
    
    return SuccessResponse(message="Record updated", metadata=format_record(record))


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