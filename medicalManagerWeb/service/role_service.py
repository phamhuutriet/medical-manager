from ..core.error_response import *
from ..core.success_response import *
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from ..models import *
from ..utils.formatter import *


def create_role(request_data):
    try:
        role_name = request_data["roleName"]
    except KeyError:
        return BadRequestErrorResponse(message="Key error: roleName field missing")

    try:
        role = Role()
        role.name = role_name
        role.save()
    except IntegrityError:
        return BadRequestErrorResponse(message="This role is already existed")
    
    return OKResponse(message="Role created")


def get_all_roles():
    all_roles = list(Role.objects.all())
    formatted_roles = [format_role(role) for role in all_roles]

    return OKResponse(message="Get all roles successfully", metadata=formatted_roles)