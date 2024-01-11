import json
from ..core.error_response import *
from ..core.success_response import *
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from ..models import *
from ..utils.formatter import *


def is_valid_template_column_type(template_column: dict):
    template_column_types = {member.value for member in TemplateColumnType}
    return all(column_type in template_column_types for column_type in template_column.values())


def create_template(request_data, user_id):
    user = MedicalUser.objects.get(pk=user_id)

    try:
        name = request_data["name"]
        medical_history_columns = request_data["medicalHistoryColumns"]
        observations_columns = request_data["observationColumns"]
        treatment_columns = request_data["treatmentColumns"]
    except KeyError as e:
        return BadRequestErrorResponse(message="Key error: " + str(e))
    
    # Validate object columns
    is_valid_column_types = is_valid_template_column_type(medical_history_columns) and is_valid_template_column_type(observations_columns) and is_valid_template_column_type(treatment_columns)
    if not is_valid_column_types:
        return BadRequestErrorResponse(message="Invalid columns type")

    try:    
        template = Template()
        template.name = name
        template.medical_history_columns = json.dumps(medical_history_columns)
        template.observation_columns = json.dumps(observations_columns)
        template.treatment_columns = json.dumps(treatment_columns)
        template.user = user
        template.save()
    except IntegrityError:
        return BadRequestErrorResponse(message="Template name is already existed")
    
    return CreatedResponse(message="Template created", metadata=format_template(template))


def get_single_template(template_id):
    template = Template.objects.get(pk=template_id)
    return OKResponse(message="Get template", metadata=format_template(template))


def get_all_templates(user_id):
    user = MedicalUser.objects.get(pk=user_id)
    templates = list(Template.objects.all().filter(user=user))
    formatted_templates = [format_template(template) for template in templates]

    return OKResponse(message="Get all templates from user", metadata=formatted_templates)


def update_template(request_data, template_id):
    template = Template.objects.get(pk=template_id)

    try:
        name = request_data["name"]
        medical_history_columns = request_data["medicalHistoryColumns"]
        observations_columns = request_data["observationColumns"]
        treatment_columns = request_data["treatmentColumns"]
    except KeyError as e:
        return BadRequestErrorResponse(message="Key error: " + str(e))
    
    # Validate object columns
    is_valid_column_types = is_valid_template_column_type(medical_history_columns) and is_valid_template_column_type(observations_columns) and is_valid_template_column_type(treatment_columns)
    if not is_valid_column_types:
        return BadRequestErrorResponse(message="Invalid columns type")

    template.name = name
    template.medical_history_columns = json.dumps(medical_history_columns)
    template.observation_columns = json.dumps(observations_columns)
    template.treatment_columns = json.dumps(treatment_columns)
    template.save()

    return CreatedResponse(message="Template updated", metadata=format_template(template))


def template_authenticate(uid, tid, callback):
    user = MedicalUser.objects.get(pk=uid)

    try:
        template = Template.objects.get(pk=tid)
    except ObjectDoesNotExist:
        return NotFoundErrorResponse(message="Template not found")
    
    if template.user != user:
        return BadRequestErrorResponse(message="You don't have the permission to access this template")

    return callback()