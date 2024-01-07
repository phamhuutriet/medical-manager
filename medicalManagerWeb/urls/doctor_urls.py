from django.urls import path
from ..views.doctor_views import *

urlpatterns = [
    path('<str:did>/', single_doctor_view, name="single_doctor_view"),
    path('', multiple_doctor_view, name="multiple_doctor_view"),
]