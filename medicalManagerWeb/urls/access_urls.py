from django.urls import path
from ..views.access_views import *


urlpatterns = [
    path('signup/', signup_view, name="signup_view"),
    path('verify/', verify_signup_view, name="verify_signup_view"),
    path('signin/', signin_view, name="signin_view"),
]