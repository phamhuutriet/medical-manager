from django.urls import path
from ..views.patient_views import *
from ..views.record_views import *
from ..views.treatment_views import *

urlpatterns = [
    path('', PatientListCreateView.as_view(), name="multiple_patients_view"),
    path('<str:id>/', PatientRetrieveUpdateDestroy.as_view(), name="single_patients_view"),
    path('<str:pid>/records/', RecordListCreateView.as_view(), name="multiple_record_view"),
    path('<str:pid>/records/<str:id>/', RecordRetrieveUpdateDestroy.as_view(), name="single_record_view"),
    path('<str:pid>/records/<str:rid>/treatments/', TreatmentListCreateView.as_view(), name="multiple_treatment_view"),
    path('<str:pid>/records/<str:rid>/treatments/<str:id>/', TreatmentListCreateView.as_view(), name="single_treatment_view"),
]