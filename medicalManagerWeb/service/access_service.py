from ..core.error_response import *
from ..core.success_response import *
from django.core.mail import send_mail
from ..models import *
import os


def pre_signup(request_data):
    try:
        display_name = request_data["displayName"]
        username = request_data["username"]
        password = request_data["password"]
        email = request_data["email"]
    except KeyError as e:
        return BadRequestErrorResponse(message='KeyError: ' + str(e))
    
    # Save sign up request 
    signupRequest = UserSignUpRequest()
    signupRequest.display_name = display_name
    signupRequest.username = username
    signupRequest.password = password
    signupRequest.email = email

    # Call API to send approval email here
    subject = "Medical Manager Sign Up Approval"
    message = "Please click on this link to finish email verification"
    from_email = os.environ.get('EMAIL_USER')
    recipient = [email]

    try:
        send_mail(subject, message, from_email, recipient)
        # # Only save after sending email successfully
        # signupRequest.save()
        return OKResponse(message="Sign up successfully")
    except Exception as e:
        return BadRequestErrorResponse(message="Error sending email " + str(e))