from djangorestframework_camel_case.util import camel_to_underscore
from ..models import *
from ..core.enums import *
import json
import base64
import imghdr


def is_base64_image(s):
    # Check if it's a base64 encoded string
    try:
        # Decode the string
        decoded_bytes = base64.b64decode(s, validate=True)
    except (base64.binascii.Error, ValueError):
        # If it's not a valid base64 string
        return False

    # Check if the decoded bytes form a valid image
    return imghdr.what(None, h=decoded_bytes) is not None

def convert_camel_to_snake(obj):
    if isinstance(obj, dict):
        return {camel_to_underscore(key): convert_camel_to_snake(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_camel_to_snake(element) for element in obj]
    else:
        return obj
    

def validate_single_template_field(concrete_object, template_object):
    processed_template_object = convert_camel_to_snake(template_object)
    for key, value in concrete_object.items():
        if key not in processed_template_object:
            return False 
        value_type = processed_template_object[key]
        if value_type == TemplateColumnType.TEXT and not isinstance(value, str):
            return False 
        if value_type == TemplateColumnType.IMAGE and not is_base64_image(value):
            return False
    return True


def validate_record_template(record: Record, template: Template):
    # Validate medical history
    record_medical_history = json.loads(record.medical_history)
    template_medical_history_columns = json.loads(template.medical_history_columns)
    is_valid_medical_history = validate_single_template_field(record_medical_history, template_medical_history_columns)
    
    # Validate observation
    record_observation = json.loads(record.observation)
    template_observation = json.loads(template.observation_columns)
    is_valid_observation = validate_single_template_field(record_observation, template_observation)
    
    return is_valid_medical_history and is_valid_observation


def validate_treatment_template(treatment: Treatment, template: Template):
    # Validate treatment columns
    treatment_data = json.loads(treatment.data)
    template_treatment_columns = json.loads(template.treatment_columns)
    is_valid_treatment = validate_single_template_field(treatment_data, template_treatment_columns)

    return is_valid_treatment