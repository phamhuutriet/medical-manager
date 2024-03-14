from rest_framework.decorators import api_view
from rest_framework import generics
from ..core.success_response import *
from ..service.patient_service import *
from rest_framework.permissions import IsAuthenticated
from ..core.permissions import UserPermission

class PatientListCreateView(generics.ListCreateAPIView):
    serializer_class = PatientSerializer

    def get_queryset(self):
        user_id = self.kwargs['uid']
        queryset = Patient.objects.all().filter(user_id=user_id)
        return queryset
    
    def perform_create(self, serializer):
        serializer.validated_data['user_id'] = self.kwargs['uid']
        serializer.save()

    def get_permissions(self):
        return [IsAuthenticated(), UserPermission()]
    

class PatientRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PatientSerializer
    lookup_field = 'id'
    
    def get_queryset(self):
        user_id = self.kwargs['uid']
        queryset = Patient.objects.all().filter(user_id=user_id)
        return queryset

    def get_permissions(self):
        return [IsAuthenticated(), UserPermission()]