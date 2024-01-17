from rest_framework.decorators import api_view
from rest_framework.request import Request
from ..core.success_response import *
from ..service.record_service import *


@api_view(["POST", "GET"])
def multiple_record_view(request, uid, pid):
    if request.method == "POST":
        return create_record(request.data, pid, uid)
    elif request.method == "GET":
        return get_all_records(pid)
    

@api_view(["GET", "PATCH"])
def single_record_view(request, uid, pid, rid):
    print("VISIT SINGLE RECORD VIEW")
    if request.method == "GET":
        return get_record(rid)
    elif request.method == "PATCH":
        return update_record(request.data, pid, rid, uid)