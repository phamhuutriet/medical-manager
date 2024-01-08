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