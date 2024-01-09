from rest_framework.decorators import api_view
from rest_framework.request import Request
from ..core.success_response import *
from ..service.role_service import *


@api_view(["GET", "POST"])
def role_view(request: Request, uid):
    if request.method == "GET":
        return get_all_roles(uid)
    elif request.method == "POST":
        return create_role(request.data, uid)