from ..core.error_response import *
from ..core.success_response import *
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from ..models import *
from ..utils.formatter import *
from ..core.template_validator import *
from ..core.serializers import *


def create_record(request_data, pid, uid):
    serializer = RecordSerializer(data=request_data)
    serializer.is_valid(raise_exception=True)
    patient = Patient.objects.get(pk=pid)
    user = MedicalUser.objects.get(pk=uid)

    try:
        record = serializer.save(patient=patient, user=user)
    except IntegrityError as e:
        return BadRequestErrorResponse(message="Error saving record " + str(e))

    record_serializer = RecordSerializer(record)
    return CreatedResponse(message="Record created", metadata=record_serializer.data)


def get_record(rid):
    record = Record.objects.get(pk=rid)
    record_serializer = RecordSerializer(record)
    return OKResponse(message="Get record successfully", metadata=record_serializer.data)


def update_record(request_data, pid, rid, uid):
    record = Record.objects.get(pk=rid)
    serializer = RecordSerializer(record, data=request_data)
    serializer.is_valid(raise_exception=True)
    patient = Patient.objects.get(pk=pid)
    user = MedicalUser.objects.get(pk=uid)

    try:
        updated_record = serializer.save(patient=patient, user=user)
    except IntegrityError as e:
        return BadRequestErrorResponse(message="Error saving record " + str(e))
    
    record_serializer = RecordSerializer(updated_record)
    return CreatedResponse(message="Record updated", metadata=record_serializer.data)


def get_all_records(pid):
    patient = Patient.objects.get(pk=pid)
    patient_records = list(Record.objects.all().filter(patient=patient))
    formatted_patient_records = [RecordSerializer(record).data for record in patient_records]
    return OKResponse(message="Get all records from patient", metadata=formatted_patient_records)


def record_authenticate(pid, rid, callback):
    patient = Patient.objects.get(pk=pid)

    try:
        record = Record.objects.get(pk=rid)
    except ObjectDoesNotExist:
        return NotFoundErrorResponse(message="Record not found")
    
    if record.patient != patient:
        return BadRequestErrorResponse(message="You don't have the permission to access this record")
    
    return callback()