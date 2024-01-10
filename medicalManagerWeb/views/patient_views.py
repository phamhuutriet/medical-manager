from rest_framework.decorators import api_view
from rest_framework.request import Request
from ..core.success_response import *
from ..service.patient_service import *


@api_view(["POST", "GET"])
def multiple_patients_view(request, uid):
    if request.method == "POST":
        return create_patient(request.data, uid)
    elif request.method == "GET":
        return get_all_patients(uid)
    

@api_view(["GET", "PATCH"])
def single_patients_view(request, pid, uid):
    if request.method == "GET":
        return get_patient(pid)
    elif request.method == "PATCH":
        return update_patients(request.data, pid, uid)