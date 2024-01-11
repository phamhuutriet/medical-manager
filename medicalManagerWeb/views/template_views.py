from rest_framework.decorators import api_view
from rest_framework.request import Request
from ..core.success_response import *
from ..service.template_service import *


@api_view(["POST", "GET"])
def multiple_template_view(request, uid):
    if request.method == "POST":
        return create_template(request.data, uid)
    elif request.method == "GET":
        return get_all_templates(uid)
    

@api_view(["GET", "PATCH"])
def single_template_view(request, uid, tid):
    if request.method == "GET":
        return get_single_template(tid)
    elif request.method == "PATCH":
        return update_template(request.data, tid)
