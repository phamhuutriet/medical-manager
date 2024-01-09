from rest_framework.decorators import api_view
from rest_framework.request import Request
from ..core.success_response import *
from ..service.treatment_service import *


@api_view(["POST", "GET"])
def multiple_treatment_view(request, uid, pid, rid):
    if request.method == "POST":
        return create_treatment(request.data, rid, request.GET)
    elif request.method == "GET":
        return get_all_treatments(rid, request.GET)
    

@api_view(["GET", "PATCH"])
def single_treatment_view(request, uid, pid, rid, tid):
    if request.method == "GET":
        return get_treatment(rid, tid, request.GET)
    elif request.method == "PATCH":
        return update_treatment(request.data, rid, tid, request.GET)