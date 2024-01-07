from ..core.error_response import *
from ..core.success_response import *
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from ..utils.token_generator import *
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

    try:
        signupRequest.save()
        host_name = os.environ.get("HOST_NAME")
        verify_url = f"{host_name}service/access/verify/?signupId={signupRequest.pk}"
        
        # Call API to send approval email here
        subject = "Medical Manager Sign Up Approval"
        message = f"Please click on this link to finish email verification {verify_url}"
        from_email = os.environ.get('EMAIL_USER')
        recipient = [email]

        send_mail(subject, message, from_email, recipient)
        return OKResponse(message="Sign up successfully")
    except Exception as e:
        return BadRequestErrorResponse(message="Error sending email " + str(e))
    

def verify_signup(signup_id):
    try:
        signup_request = UserSignUpRequest.objects.get(pk=signup_id)
    except ObjectDoesNotExist:
        return BadRequestErrorResponse(message="Sign up request not found")
    
    medicalUser = MedicalUser()
    medicalUser.display_name = signup_request.display_name
    medicalUser.username = signup_request.username
    medicalUser.password = signup_request.password
    medicalUser.email = signup_request.email
    medicalUser.save()

    # Create KeyToken for new user
    key_token = KeyToken()
    key_token.user = medicalUser
    key_token.save()

    return OKResponse(message="User signed up successfully")


def sign_in(request):
    try:
        username = request.data["username"]
        password = request.data["password"]
    except KeyError as e:
        return BadRequestErrorResponse(message="Key Error: " + str(e))
    
    user = authenticate(request, username=username, password=password)

    if user is None:
        return BadRequestErrorResponse(message="Invalid username or password")
    
    # Generate tokens
    token_payload = {"username": username, "id": user.pk}
    public_key, private_key = generate_rsa_key_pair()
    access_token, refresh_token = create_token_pair(
        token_payload,
        private_key,
        public_key,
    )

    # Save tokens and keys
    key_token = KeyToken.objects.get(user=user)
    key_token.public_key = public_key
    key_token.refresh_token = refresh_token
    key_token.save()

    response = {
        "accessToken": access_token,
        "refreshToken": refresh_token,
        "authorId": user.pk,
    }

    return OKResponse(message="sign in", metadata=response)