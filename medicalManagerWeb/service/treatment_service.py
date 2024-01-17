from ..core.error_response import *
from ..core.success_response import *
from django.core.exceptions import ObjectDoesNotExist
from ..models import *
from ..utils.formatter import *
from ..core.template_validator import *
from ..core.serializers import *


def create_treatment(request_data, rid):
    record = Record.objects.get(pk=rid)
    template = record.template
    serializer = TreatmentSerializer(data=request_data)
    serializer.is_valid(raise_exception=True)

    try:
        treatment = serializer.save(record=record, template=template)
    except Exception as e:
        return BadRequestErrorResponse(message="Error saving treatment " + str(e))
    
    treatment_serializer = TreatmentSerializer(treatment)
    return CreatedResponse(message="Treatment created", metadata=treatment_serializer.data)


def get_treatment(tid):    
    treatment = Treatment.objects.get(pk=tid)
    treatment_serializer = TreatmentSerializer(treatment)
    return OKResponse(message="Get treatment successfully", metadata=treatment_serializer.data)


def update_treatment(request_data, rid, tid):
    treatment = Treatment.objects.get(pk=tid)
    record = Record.objects.get(pk=rid)
    template = record.template
    serializer = TreatmentSerializer(treatment, data=request_data)
    serializer.is_valid(raise_exception=True)

    try:
        updated_treatment = serializer.save(record=record, template=template)
    except Exception as e:
        return BadRequestErrorResponse(message="Error saving treatment " + str(e))
    
    treatment_serializer = TreatmentSerializer(updated_treatment)
    return CreatedResponse(message="Treatment created", metadata=treatment_serializer.data)


def get_all_treatments(rid, query_params):
    record = Record.objects.get(pk=rid)
    treatments = Treatment.objects.all().filter(record=record)
    formatted_treatments = [TreatmentSerializer(treatment).data for treatment in treatments]
    return OKResponse(message="Get all treatments", metadata=formatted_treatments)


def treatment_authenticate(rid, tid, callback):
    record = Record.objects.get(pk=rid)

    try:
        treatment = Treatment.objects.get(pk=tid)
    except ObjectDoesNotExist:
        return NotFoundErrorResponse(message="Treatment not found")
    
    if treatment.record != record:
        return BadRequestErrorResponse(message="You don't have the permission to access this treatment")
    
    return callback()