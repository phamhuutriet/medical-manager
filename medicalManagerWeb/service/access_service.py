from ..core.error_response import *
from ..core.success_response import *
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from ..utils.token_generator import *
from ..models import *
from rest_framework_simplejwt.tokens import RefreshToken
from ..core.enums import *
import os


def pre_signup(request_data):
    try:
        username = request_data["username"]
        password = request_data["password"]
        email = request_data["email"]
    except KeyError as e:
        return BadRequestErrorResponse(message='KeyError: ' + str(e))
    
    # Save sign up request 
    signupRequest = UserSignUpRequest()
    signupRequest.username = username
    signupRequest.password = password
    signupRequest.email = email

    try:
        signupRequest.save()
    except Exception as e:
        return BadRequestErrorResponse(message='Duplicate email' + str(e))

    try:
        host_name = os.environ.get("HOST_NAME")
        verify_url = f"{host_name}/access/verify/?signupId={signupRequest.pk}"
        
        # Call API to send approval email here
        subject = "Medical Manager Sign Up Approval"
        message = f"Please click on this link to finish email verification {verify_url}"
        from_email = os.environ.get('EMAIL_USER')
        recipient = [email]

        send_mail(subject, message, from_email, recipient)
        return OKResponse(message="Sign up request sent. Please check your email to verify")
    except Exception as e:
        return BadRequestErrorResponse(message="Error sending email " + str(e))
    

def verify_signup(signup_id):
    try:
        signup_request = UserSignUpRequest.objects.get(pk=signup_id)
    except ObjectDoesNotExist:
        return BadRequestErrorResponse(message="Sign up request not found")
    
    medicalUser = MedicalUser()
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
        email = request.data["email"]
        password = request.data["password"]
    except KeyError as e:
        return BadRequestErrorResponse(message="Key Error: " + str(e))
    
    user = authenticate(request, email=email, password=password)

    if user is None:
        return BadRequestErrorResponse(message="Invalid email or password")
    
    refresh = RefreshToken.for_user(user)

    response = {
        "accessToken": str(refresh.access_token),
        "refreshToken": str(refresh),
        "userId": str(user.pk),
    }
    
    return OKResponse(message="sign in", metadata=response)


def user_authenticate(request, callback):
    auth_header = request.headers

    try:
        user_id = auth_header[Header.CLIENT_ID.value]
        access_token = auth_header[Header.AUTHORIZATION.value]
    except KeyError:
        return AuthFailureErrorResponse(message="Missing auth headers")

    try:
        user = MedicalUser.objects.get(pk=user_id)
    except ObjectDoesNotExist:
        return AuthFailureErrorResponse(message="Invalid user id")

    try:
        token = KeyToken.objects.get(user=user)
    except ObjectDoesNotExist:
        return NotFoundErrorResponse(message="Token store not found")

    try:
        decoded_author = jwt.decode(
            access_token, token.public_key, algorithms=["RS256"]
        )
    except jwt.PyJWTError as err:
        return AuthFailureErrorResponse(
            message="Failed to verify user and access token"
        )

    if str(decoded_author["id"]) != str(user_id):
        return AuthFailureErrorResponse(message="Invalid user id")

    return callback()