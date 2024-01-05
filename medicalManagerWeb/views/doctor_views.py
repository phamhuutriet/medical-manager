from rest_framework.decorators import api_view
from rest_framework.request import Request
from ..core.success_response import *


@api_view(["GET"])
def single_doctor_view(request, did):
    return OKResponse(message="OK", metadata={"message": "test ok"})