from django.urls import path
from ..views.doctor_views import *

urlpatterns = [
    path('<str:id>/', DoctorRetrieveUpdateDestroy.as_view(), name="single_doctor_view"),
    path('', DoctorListCreateView.as_view(), name="multiple_doctor_view"),
]