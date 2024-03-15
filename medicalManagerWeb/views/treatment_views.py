from rest_framework.decorators import api_view
from rest_framework import generics
from ..core.success_response import *
from ..service.patient_service import *
from rest_framework.permissions import IsAuthenticated
from ..core.permissions import UserPermission


class TreatmentListCreateView(generics.ListCreateAPIView):
    serializer_class = TreatmentSerializer

    def get_queryset(self):
        user_id = self.kwargs['uid']
        patient_id = self.kwargs['pid']
        record_id = self.kwargs['rid']
        queryset = Patient.objects.all().filter(user_id=user_id, patient_id=patient_id, record_id=record_id)
        return queryset
    
    def perform_create(self, serializer):
        serializer.validated_data['user_id'] = self.kwargs['uid']
        serializer.validated_data['patient_id'] = self.kwargs['pid']
        serializer.validated_data['record_id'] = self.kwargs['rid']
        serializer.save()

    def get_permissions(self):
        return [IsAuthenticated(), UserPermission()]
    

class TreatmentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TreatmentSerializer
    lookup_field = 'id'
    
    def get_queryset(self):
        user_id = self.kwargs['uid']
        patient_id = self.kwargs['pid']
        record_id = self.kwargs['rid']
        queryset = Patient.objects.all().filter(user_id=user_id, patient_id=patient_id, record_id=record_id)
        return queryset

    def get_permissions(self):
        return [IsAuthenticated(), UserPermission()]