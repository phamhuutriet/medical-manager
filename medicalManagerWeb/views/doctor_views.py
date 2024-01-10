from rest_framework.decorators import api_view
from rest_framework.request import Request
from ..core.success_response import *
from ..service.doctor_service import *


@api_view(["GET", "PATCH"])
def single_doctor_view(request, uid, did):
    if request.method == "GET":
        return get_single_doctor(did)
    elif request.method == "PATCH":
        return update_doctor(request.data, did)


@api_view(["POST", "GET"]) 
def multiple_doctor_view(request, uid):
    if request.method == "POST":
        return create_doctor(request.data, uid)
    elif request.method == "GET":
        return get_all_doctors(uid)
    
