from rest_framework.decorators import api_view
from ..core.success_response import *
from ..service.doctor_service import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics
from ..core.serializers import * 
    

class DoctorListCreateView(generics.ListCreateAPIView):
    serializer_class = DoctorSerializer

    def get_queryset(self):
        user_id = self.kwargs['uid']
        queryset = Doctor.objects.all().filter(user_id=user_id)
        return queryset
    
    def perform_create(self, serializer):
        serializer.validated_data['user_id'] = self.kwargs['uid']
        serializer.save()

    def get_permissions(self):
        return [IsAuthenticated()]
    

class DoctorRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DoctorSerializer
    lookup_field = 'id'
    
    def get_queryset(self):
        user_id = self.kwargs['uid']
        queryset = Doctor.objects.all().filter(user_id=user_id)
        return queryset

    def get_permissions(self):
        return [IsAuthenticated()]