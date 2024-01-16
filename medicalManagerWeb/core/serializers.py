from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from ..models import *


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']


class DoctorSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(
        write_only=True, 
        queryset=Role.objects.all(), 
        source='role'
    )

    class Meta:
        model = Doctor
        fields = ['id', 'name', 'role', 'role_id', 'phone_number']
        read_only_fields = ['id']


    def create(self, validated_data):
        role = validated_data.pop('role', None)
        doctor = Doctor.objects.create(**validated_data)
        if role is not None:
            doctor.role = role
            doctor.save()
        return doctor
    
    def update(self, instance: Doctor, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.phone_number = validated_data.get("phone_number", instance.phone_number)
        role = validated_data.get("role", None)
        if role is not None:
            instance.role = role
        instance.save()
        return instance