from rest_framework.decorators import api_view
from rest_framework.request import Request
from ..core.success_response import *
from ..service.doctor_service import *


@api_view(["GET"])
def single_doctor_view(request, did):
    if request.method == "GET":
        return get_single_doctor(did)


@api_view(["POST", "GET"]) 
def multiple_doctor_view(request):
    if request.method == "POST":
        return create_doctor(request.data)
    elif request.method == "GET":
        return get_all_doctors()
    
