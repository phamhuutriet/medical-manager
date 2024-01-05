from django.urls import path
from ..views.access_views import *


urlpatterns = [
    path('signup/', signup_view, name="signup_view"),
]