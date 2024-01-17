from ..core.error_response import *
from ..core.success_response import *
from django.db import IntegrityError
from ..models import *
from ..utils.formatter import *
from ..core.serializers import *


def create_role(request_data, uid):
    user = MedicalUser.objects.get(pk=uid)
    serializer = RoleSerializer(data=request_data)
    serializer.is_valid(raise_exception=True)
    
    try:
        role = serializer.save(user=user)
    except IntegrityError as e: 
        return BadRequestErrorResponse(message="Error saving role: " + str(e))
    
    role_serializer = RoleSerializer(role)
    return SuccessResponse(message="Role created", metadata=role_serializer.data)


def get_all_roles(uid):
    user = MedicalUser.objects.get(pk=uid)
    all_roles = list(Role.objects.all().filter(user=user))
    formatted_roles = [RoleSerializer(role).data for role in all_roles]
    return OKResponse(message="Get all roles successfully", metadata=formatted_roles)