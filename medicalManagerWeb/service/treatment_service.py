from ..core.error_response import *
from ..core.success_response import *
from django.core.exceptions import ObjectDoesNotExist
from ..models import *
from ..utils.formatter import *
from ..core.template_validator import *
import json


def create_treatment(request_data, rid, query_params):
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
    
    template = record.template

    try:
        treatment = Treatment()
        treatment.template = template
        treatment.record = record
        treatment.data = json.dumps(request_data)

        if not validate_treatment_template(treatment, template):
            return BadRequestErrorResponse(message="Treatment and template not match")
        
        treatment.save()
    except Exception as e:
        return BadRequestErrorResponse(message="Error saving treatment " + str(e))
    
    return CreatedResponse(message="Treatment created", metadata=format_treatment(treatment))


def get_treatment(rid, tid, query_params):
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
    
    treatment = Treatment.objects.get(pk=tid)
    if not validate_treatment_template(treatment, record.template):
        return BadRequestErrorResponse(message="Treatment and template not match")
            
    if treatment.record != record:
        return BadRequestErrorResponse(message="You don't have permission to view this treatment")
    
    return OKResponse(message="Get treatment successfully", metadata=format_treatment(treatment))


def update_treatment(request_data, rid, tid, query_params):
    version = None
    if "version" in query_params:
        version = query_params["version"]
        if not version.isdigit():
            return BadRequestErrorResponse(message="TypeError: version must be integer")

    try:
        if version is None:
            record = Record.objects.filter(record_id=rid).order_by('-version').first()
        else:
            record = Record.objects.get(record_id=rid, version=version)
    except ObjectDoesNotExist:
        return BadRequestErrorResponse(message="Record not found")
    
    template = record.template
    treatment = Treatment.objects.get(pk=tid)

    try:
        treatment.data = json.dumps(request_data)
        if not validate_treatment_template(treatment, template):
            return BadRequestErrorResponse(message="Treatment and template not match")
        treatment.save()
    except Exception as e:
        return BadRequestErrorResponse(message="Error saving treatment " + str(e))
    
    return CreatedResponse(message="Treatment updated", metadata=format_treatment(treatment))


def get_all_treatments(rid, query_params):
    version = None
    if "version" in query_params:
        version = query_params["version"]
        if not version.isdigit():
            return BadRequestErrorResponse(message="TypeError: version must be integer")

    try:
        if version is None:
            record = Record.objects.filter(record_id=rid).order_by('-version').first()
        else:
            record = Record.objects.get(record_id=rid, version=version)
    except ObjectDoesNotExist:
        return BadRequestErrorResponse(message="Record not found")
    
    treatments = Treatment.objects.all().filter(record=record)
    formatted_treatments = [format_treatment(treatment) for treatment in treatments]

    return OKResponse(message="Get all treatments", metadata=formatted_treatments)


def treatment_authenticate(version, rid, tid, callback):
    if not version:
        record = Record.objects.filter(
            record_id=rid
        ).order_by('-version')[:1].get()
    else:
        record = Record.objects.get(
            record_id=rid,
            version=version
        )

    try:
        treatment = Treatment.objects.get(pk=tid)
    except ObjectDoesNotExist:
        return NotFoundErrorResponse(message="Treatment not found")
    
    if treatment.record != record:
        return BadRequestErrorResponse(message="You don't have the permission to access this treatment")
    
    return callback()