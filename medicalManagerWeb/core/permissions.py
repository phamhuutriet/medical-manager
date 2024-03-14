from rest_framework.permissions import BasePermission
from ..models import *
import uuid


class UserPermission(BasePermission):
    """
    Only allows perform action if the requested user is the same user of the url
    """
    def has_permission(self, request, view):
        if request.user:
            # Convert uid into uuid object and stringify it to get uuid string format
            return str(request.user.pk) == str(uuid.UUID(view.kwargs.get('uid')))
        return False