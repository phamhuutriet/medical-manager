from rest_framework.decorators import api_view
from rest_framework.request import Request
from ..core.success_response import *
from ..service.record_service import *


@api_view(["POST"])
def multiple_record_view(request, pid, uid):
    if request.method == "POST":
        return create_record(request.data, pid)