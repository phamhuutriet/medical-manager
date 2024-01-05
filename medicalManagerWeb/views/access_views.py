from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.status import *

from ..service.access_service import *

@api_view(["POST"])
def signup_view(request):
    if request.method == "POST":
        return pre_signup(request.data)