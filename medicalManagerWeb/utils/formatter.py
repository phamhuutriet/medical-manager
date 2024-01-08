from ..models import *
import json


def format_role(role: Role):
    return {
        "id": str(role.pk),
        "name": role.name
    }


def format_doctor(doctor: Doctor):
    return {
        "id": str(doctor.pk),
        "name": doctor.name,
        "role": format_role(doctor.role),
        "phoneNumber": str(doctor.phone_number)
    }


def format_patient(patient: Patient):
    return {
        "id": str(patient.pk),
        "name": patient.name,
        "gender": patient.gender,
        "dateOfBirth": patient.date_of_birth,
        "address": patient.address,
        "phoneNumber": str(patient.phone_number),
        "note": patient.note,
        "allergies": json.loads(patient.allergies)
    }


def format_record(record: Record):
    # TODO: return TEST result + TREATMENT -> must have models first

    return {
        "id": str(record.record_id),
        "patient": format_patient(record.patient),
        "reasonForVisit": record.reason_for_visit,
        "medicalHistory": json.loads(record.medical_history),
        "symptom": record.symptom,
        "vitalSign": json.loads(record.vital_signs),
        "observation": json.loads(record.observation),
        "diagnosis": record.diagnosis,
        "primaryDoctor": format_doctor(record.primary_doctor),
        "treatmentPlan": json.loads(record.treatment_plan),
    }


def format_template(template: Template):
    return {
        "id": str(template.pk),
        "name": template.name,
        "medicalHistoryColumns": json.loads(template.medical_history_columns),
        "observationColumns": json.loads(template.observation_columns),
        "treatmentColumns": json.loads(template.treatment_columns)
    }