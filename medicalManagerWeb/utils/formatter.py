from ..models import *

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