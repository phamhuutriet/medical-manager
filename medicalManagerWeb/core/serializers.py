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
    role = RoleSerializer(read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(
        write_only=True, 
        queryset=Role.objects.all(), 
        source='role'
    )

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
        fields = ['id', 'first_name', 'last_name', 'role', 'role_id', 'phone_number', 'gender', 'date_of_birth']
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
    

class RecordSerializer(serializers.ModelSerializer):
    template = TemplateSerializer(read_only=True)
    template_id = serializers.PrimaryKeyRelatedField(
        write_only=True, 
        queryset=Template.objects.all(), 
        source='template'
    )
    patient = PatientSerializer(read_only=True)
    primary_doctor = DoctorSerializer(read_only=True)
    primary_doctor_id = serializers.PrimaryKeyRelatedField(
        write_only=True, 
        queryset=Doctor.objects.all(), 
        source='primary_doctor'
    )
    medical_history = JSONDictField()
    observation = JSONDictField()
    vital_signs = JSONDictField()
    treatment_plan = JSONListField()

    class Meta:
        model = Record
        fields = ['id', 'template', 'template_id', 'patient', 'reason_for_visit', 'symptom',
                   'medical_history', 'vital_signs', 'date', 'observation', 'diagnosis',
                    'primary_doctor', 'primary_doctor_id', 'treatment_plan']
        read_only_fields = ['id']


    def create(self, validated_data):
        user = validated_data.pop("user")

        # Validate doctor
        doctor: Doctor = validated_data.get("primary_doctor")
        if doctor.user != user:
            raise ValidationError("You can't access this doctor")

        record = Record()
        record.patient = validated_data.get("patient")
        record.reason_for_visit = validated_data.get("reason_for_visit")
        record.symptom = validated_data.get("symptom")
        record.medical_history = validated_data.get("medical_history")
        record.vital_signs = validated_data.get("vital_signs")
        record.observation = validated_data.get("observation")
        record.diagnosis = validated_data.get("diagnosis")
        record.primary_doctor = validated_data.get("primary_doctor")
        record.treatment_plan = validated_data.get("treatment_plan")
        record.template = validated_data.get("template")
        
        # Validate template
        template: Template = record.template
        if template.user != user or not validate_record_template(record, template):
            raise ValidationError("Template and record are not matched")

        record.save()
        return record

    
    def update(self, record: Record, validated_data):
        user = validated_data.pop("user")

        # Validate doctor
        doctor: Doctor = validated_data.get("primary_doctor")
        if doctor.user != user:
            raise ValidationError("You can't access this doctor")

        record.patient = validated_data.get("patient", record.patient)
        record.reason_for_visit = validated_data.get("reason_for_visit", record.reason_for_visit)
        record.symptom = validated_data.get("symptom", record.symptom)
        record.medical_history = validated_data.get("medical_history", record.medical_history)
        record.vital_signs = validated_data.get("vital_signs", record.vital_signs)
        record.observation = validated_data.get("observation", record.observation)
        record.diagnosis = validated_data.get("diagnosis", record.diagnosis)
        record.primary_doctor = validated_data.get("primary_doctor", record.primary_doctor)
        record.treatment_plan = validated_data.get("treatment_plan", record.treatment_plan)
        record.template = validated_data.get("template", record.template)
        
        # Validate template
        template: Template = record.template
        if template.user != user or not validate_record_template(record, template):
            raise ValidationError("Template and record are not matched")

        record.save()
        return record
    

class TreatmentSerializer(serializers.ModelSerializer):
    template = TemplateSerializer(read_only=True)
    record = RecordSerializer(read_only=True)
    data = JSONDictField()

    class Meta:
        model = Treatment
        fields = ['id', 'template', 'record', 'data']
        read_only_fields = ['id']

    def create(self, validated_data):
        treatment = Treatment()
        treatment.template = validated_data.get("template")
        treatment.record = validated_data.get("record")
        treatment.data = validated_data.get("data")

        if not validate_treatment_template(treatment, treatment.template):
            raise ValidationError("Template and treatment mismatch")
        
        treatment.save()
        return treatment
    
    def update(self, treatment: Treatment, validated_data):
        treatment.template = validated_data.get("template", treatment.template)
        treatment.record = validated_data.get("record", treatment.record)
        treatment.data = validated_data.get("data", treatment.data)

        if not validate_treatment_template(treatment, treatment.template):
            raise ValidationError("Template and treatment mismatch")
        
        treatment.save()
        return treatment