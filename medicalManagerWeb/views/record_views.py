from rest_framework.decorators import api_view
from rest_framework import generics
from ..core.success_response import *
from ..service.patient_service import *
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from ..core.permissions import UserPermission


class RecordListCreateView(generics.ListCreateAPIView):
    serializer_class = RecordSerializer

    def get_queryset(self):
        user_id = self.kwargs['uid']
        patient_id = self.kwargs['pid']
        user = get_object_or_404(MedicalUser, id=user_id)
        patient = get_object_or_404(Patient, id=patient_id)
        queryset = Record.objects.filter(patient=patient, patient__user=user)
        return queryset
    
    def perform_create(self, serializer):
        serializer.validated_data['patient_id'] = self.kwargs['pid']
        serializer.save()

    def get_permissions(self):
        return [IsAuthenticated(), UserPermission()]
    

class RecordRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RecordSerializer
    lookup_field = 'id'
    
    def get_queryset(self):
        user_id = self.kwargs['uid']
        patient_id = self.kwargs['pid']
        user = get_object_or_404(MedicalUser, id=user_id)
        patient = get_object_or_404(Patient, id=patient_id)
        queryset = Record.objects.filter(patient=patient, patient__user=user)
        return queryset

    def get_permissions(self):
        return [IsAuthenticated(), UserPermission()]