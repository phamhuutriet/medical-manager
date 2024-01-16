from ..core.error_response import *
from ..core.success_response import *
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from ..models import *
from ..utils.formatter import *
from ..core.serializers import *


def create_template(request_data, user_id):
    user = MedicalUser.objects.get(pk=user_id)
    serializer = TemplateSerializer(data=request_data)
    serializer.is_valid(raise_exception=True)

    try:
        template = serializer.save(user=user)
    except IntegrityError as e:
        return BadRequestErrorResponse(message="Error saving template: " + str(e))
    
    template_serializer = TemplateSerializer(template)
    return CreatedResponse(message="Template created", metadata=template_serializer.data)


def get_single_template(template_id):
    template = Template.objects.get(pk=template_id)
    serializer  =TemplateSerializer(template)
    return OKResponse(message="Get template", metadata=serializer.data)


def get_all_templates(user_id):
    user = MedicalUser.objects.get(pk=user_id)
    templates = list(Template.objects.all().filter(user=user))
    formatted_templates = [TemplateSerializer(template).data for template in templates]
    return OKResponse(message="Get all templates from user", metadata=formatted_templates)


def update_template(request_data, template_id):
    template = Template.objects.get(pk=template_id)
    serializer = TemplateSerializer(template, data=request_data)
    serializer.is_valid(raise_exception=True)

    try:
        updated_template = serializer.save()
    except IntegrityError as e:
        return BadRequestErrorResponse(message="Error saving template " + str(e))
    
    template_serializer = TemplateSerializer(updated_template)
    return CreatedResponse(message="Template updated", metadata=template_serializer.data)


def template_authenticate(uid, tid, callback):
    user = MedicalUser.objects.get(pk=uid)

    try:
        template = Template.objects.get(pk=tid)
    except ObjectDoesNotExist:
        return NotFoundErrorResponse(message="Template not found")
    
    if template.user != user:
        return BadRequestErrorResponse(message="You don't have the permission to access this template")

    return callback()