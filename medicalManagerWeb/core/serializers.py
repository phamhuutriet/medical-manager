from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from ..models import *
import json
from ..utils.template_validator import *


class JSONListField(serializers.Field):
    def to_representation(self, value):
        return json.loads(value)

    def to_internal_value(self, data):
        if isinstance(data, list):
            return json.dumps(data)
        raise serializers.ValidationError("Expected a list of data")
    

class JSONDictField(serializers.Field):
    def to_representation(self, value):
        return json.loads(value)

    def to_internal_value(self, data):
        if isinstance(data, dict):
            return json.dumps(data)
        raise serializers.ValidationError("Expected a dict of data")
    

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
    

class PatientSerializer(serializers.ModelSerializer):
    allergies = JSONListField()

    class Meta:
        model = Patient
        fields = ['id', 'name', 'gender', 'address', 'date_of_birth', 'phone_number', 'note', 'allergies']
        read_only_fields = ['id']
    
    def create(self, validated_data):
        patient = Patient.objects.create(**validated_data)
        return patient
    
    def update(self, instance: Patient, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.address = validated_data.get('address', instance.address)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.note = validated_data.get('note', instance.note)
        instance.allergies = validated_data.get('allergies', instance.allergies)
        instance.save()
        return instance
    


class TemplateSerializer(serializers.ModelSerializer):
    medical_history_columns = JSONDictField()
    observation_columns = JSONDictField()
    treatment_columns = JSONDictField()

    class Meta:
        model = Template
        fields = ['id', 'name', 'medical_history_columns', 'observation_columns', 'treatment_columns']

    def create(self, validated_data):
        return Template.objects.create(**validated_data)
    
    def update(self, instance: Template, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.medical_history_columns = validated_data.get('medical_history_columns', instance.medical_history_columns)
        instance.observation_columns = validated_data.get('observation_columns', instance.observation_columns)
        instance.treatment_columns = validated_data.get('treatment_columns', instance.treatment_columns)
        instance.save()
        return instance
    
    def validate_medical_history_columns(self, value):
        if not is_valid_template_column_type(json.loads(value)):
            raise serializers.ValidationError("Medical history columns value type must follow TemplateColumnType")        
        return value
    
    def validate_observation_columns(self, value):
        if not is_valid_template_column_type(json.loads(value)):
            raise serializers.ValidationError("Observations columns value type must follow TemplateColumnType")        
        return value
    
    def validate_treatment_columns(self, value):
        if not is_valid_template_column_type(json.loads(value)):
            raise serializers.ValidationError("Treatments columns value type must follow TemplateColumnType")        
        return value