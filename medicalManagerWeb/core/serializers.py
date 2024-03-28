from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from ..models import *
import json
from ..utils.template_validator import *
from ..core.template_validator import *
from datetime import datetime


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
    # role = RoleSerializer(read_only=True)
    # role_id = serializers.PrimaryKeyRelatedField(
    #     write_only=True, 
    #     queryset=Role.objects.all(), 
    #     source='role'
    # )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['date_of_birth'] = instance.date_of_birth.strftime('%d / %m / %Y')
        return representation

    def to_internal_value(self, data):
        if 'date_of_birth' in data:
            data['date_of_birth'] = datetime.strptime(data['date_of_birth'], '%d / %m / %Y').date()
        return super().to_internal_value(data)


    class Meta:
        model = Doctor
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'gender', 'date_of_birth']
        read_only_fields = ['id']


class PatientSerializer(serializers.ModelSerializer):
    allergies = JSONListField()
    doctor = DoctorSerializer(read_only=True)
    doctor_id = serializers.PrimaryKeyRelatedField(
        write_only=True, 
        queryset=Doctor.objects.all(), 
        source='doctor'
    )


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['date_of_birth'] = instance.date_of_birth.strftime('%d / %m / %Y')
        representation['created_at'] = instance.created_at.strftime('%d / %m / %Y')
        return representation

    def to_internal_value(self, data):
        if 'date_of_birth' in data:
            data['date_of_birth'] = datetime.strptime(data['date_of_birth'], '%d / %m / %Y').date()
        return super().to_internal_value(data)

    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'gender', 'address', 'date_of_birth', \
                  'phone_number', 'note', 'allergies', 'created_at', 'doctor', 'doctor_id']
        read_only_fields = ['id', 'created_at']


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
    

class TreatmentSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)
    doctor_id = serializers.PrimaryKeyRelatedField(
        write_only=True, 
        queryset=Doctor.objects.all(), 
        source='doctor'
    )
    record_id = serializers.PrimaryKeyRelatedField(
        queryset=Record.objects.all(), 
        source='record'
    )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['date'] = instance.date.strftime('%d / %m / %Y')
        return representation

    def to_internal_value(self, data):
        data['date'] = datetime.strptime(data['date'], '%d / %m / %Y').date()
        return super().to_internal_value(data)

    class Meta:
        model = Treatment
        fields = ['id', 'record_id', 'name', 'cost', 'note', 'date', 'doctor', 'doctor_id']
        read_only_fields = ['id']


class TestSerializer(serializers.ModelSerializer):
    record_id = serializers.PrimaryKeyRelatedField(
        queryset=Record.objects.all(), 
        source='record'
    )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created_at'] = instance.created_at.strftime('%d / %m / %Y')
        return representation

    def to_internal_value(self, data):
        data['created_at'] = datetime.strptime(data['created_at'], '%d / %m / %Y').date()
        return super().to_internal_value(data)
    
    class Meta:
        model = Test
        fields = ['id', 'name', 'created_at', 'record_id', 'image']


class RecordSerializer(serializers.ModelSerializer):
    vital_signs = JSONDictField()
    treatment_plan = JSONListField()
    treatments = TreatmentSerializer(many=True, read_only=True)
    tests = TestSerializer(many=True, read_only=True)

    class Meta:
        model = Record
        fields = ['id', 'patient_id', 'reason_for_visit', 'symptom', 'medical_history',\
                'vital_signs', 'diagnosis', 'treatment_plan', 'treatments', 'created_at', 'tests']
        read_only_fields = ['id']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        record_id = instance.id  

        treatments = Treatment.objects.filter(record_id=record_id)
        representation['treatments'] = TreatmentSerializer(treatments, many=True).data

        tests = Test.objects.filter(record_id=record_id)
        representation['tests'] = TestSerializer(tests, many=True).data

        representation['created_at'] = instance.created_at.strftime('%d / %m / %Y')
        return representation