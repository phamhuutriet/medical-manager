from django.urls import path
from ..views.patient_views import *
from ..views.record_views import *

urlpatterns = [
    path('', multiple_patients_view, name="multiple_patients_view"),
    path('<str:pid>/', single_patients_view, name="single_patients_view"),
    path('<str:pid>/records/', multiple_record_view, name="multiple_record_view"),
]