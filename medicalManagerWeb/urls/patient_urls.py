from django.urls import path
from ..views.patient_views import *

urlpatterns = [
    path('', multiple_patients_view, name="multiple_patients_view"),
    path('<str:pid>/', single_patients_view, name="single_patients_view"),
]