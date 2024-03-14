from ..models import *
from ..utils.token_generator import *
from ..core.enums import *
import json
from typing import List


def create_user(user_data):
    user = MedicalUser.objects.create(
        username=user_data["username"],
        password=user_data["password"],
        email=user_data["email"]
    )

    user.save()
    token_payload = {"username": user.username, "id": str(user.pk)}

    # Generate tokens
    public_key, private_key = generate_rsa_key_pair()
    access_token, refresh_token = create_token_pair(
        token_payload,
        private_key,
        public_key,
    )

    # Save tokens and keys
    key_token = KeyToken()
    key_token.user = user
    key_token.public_key = public_key
    key_token.refresh_token = refresh_token
    key_token.save()

    return {
        "headers": {
            f"HTTP_{Header.CLIENT_ID.value}": str(user.pk),
            f"HTTP_{Header.AUTHORIZATION.value}": access_token,
        },
        "user": user,
    }


def create_doctor(doctor_data, user: MedicalUser, role: Role):
    doctor = Doctor.objects.create(
        name=doctor_data["name"],
        phone_number=doctor_data["phoneNumber"],
        role=role,
        user=user
    )
    doctor.save()

    return doctor


def create_role(role_name: str, user: MedicalUser):
    role = Role.objects.create(name=role_name, user=user)
    role.save()
    
    return role


def create_patient(patient_data, user: MedicalUser):
    patient = Patient.objects.create(
        name=patient_data["name"],
        gender=patient_data["gender"],
        date_of_birth=patient_data["dateOfBirth"],
        address=patient_data["address"],
        phone_number=patient_data["phoneNumber"],
        note=patient_data["note"],
        allergies=json.dumps(patient_data["allergies"]),
        user=user
    )
    patient.save()

    return patient


def create_record(record_data, patient: Patient, template: Template, doctor: Doctor):
    record = Record.objects.create(
        template = template,
        patient = patient,
        reason_for_visit = record_data["reasonForVisit"],
        symptom = record_data["symptom"],
        medical_history = json.dumps(record_data["medicalHistory"]),
        vital_signs = json.dumps(record_data["vitalSigns"]),
        observation = json.dumps(record_data["observation"]),
        diagnosis = record_data["diagnosis"],
        primary_doctor = doctor,
        treatment_plan = json.dumps(record_data["treatmentPlan"]),
    )
    record.save()

    return record


def create_template(template_data, user: MedicalUser):
    template = Template.objects.create(
        name=template_data["name"],
        medical_history_columns=json.dumps(template_data["medicalHistoryColumns"]),
        observation_columns=json.dumps(template_data["observationColumns"]),
        treatment_columns=json.dumps(template_data["treatmentColumns"]),
        user=user
    )
    template.save()

    return template


def create_treatment(treatment_data, record: Record, template: Template):
    treatment = Treatment.objects.create(
        template=template,
        record=record,
        data=json.dumps(treatment_data)
    )
    treatment.save()
    
    return treatment


def is_equal_fields(obj1: dict, obj2: dict, fields: List):
    for field in fields:
        if field not in obj1 or field not in obj2 or obj1[field] != obj2[field]:
            return False
    return True