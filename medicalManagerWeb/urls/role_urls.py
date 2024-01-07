from django.urls import path
from ..views.role_views import *

urlpatterns = [
    path('', role_view, name="role_view"),
]