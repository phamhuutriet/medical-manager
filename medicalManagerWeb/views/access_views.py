from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.status import *

from ..service.access_service import *

@api_view(["POST"])
@permission_classes([AllowAny])
def signup_view(request):
    if request.method == "POST":
        return pre_signup(request.data)
    

@api_view(["GET"])
@permission_classes([AllowAny])
def verify_signup_view(request):
    if request.method == "GET":
        signup_id = request.GET.get("signupId")
        return verify_signup(signup_id)
    

@api_view(["POST"])
@permission_classes([AllowAny])
def signin_view(request):
    if request.method == "POST":
        return sign_in(request)