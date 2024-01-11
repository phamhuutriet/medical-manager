from django.test import TestCase
from rest_framework.test import APIClient
from ..test_utils import *
import uuid


# THINGS TO TEST
# test get treatment -> 200
# test get treatment not belong to record -> 400
# test get non existed treatment -> 404


class TreatmentMiddlewareTest(TestCase):

    def setUp(self):
        # Create user 
        self.user_data = {
            "username": "user1",
            "password": "password1",
            "displayName": "User 1",
            "email": "user@gmail.com"
        }
        created_user_data = create_user(self.user_data)
        self.user = created_user_data["user"]
        self.user_id = str(self.user.pk)
        self.user_headers = created_user_data["headers"]
        self.client = APIClient()

        # Add credentials since we've tested no credentials in user auth middleware
        self.client.credentials(**self.user_headers)

        # Create patient
        self.patient = create_patient({
            "name": "patient",
            "gender": "M",
            "address": "281/24 lvs",
            "dateOfBirth": "1999-12-02",
            "phoneNumber": "+8454897822",
            "note": "VIP",
            "allergies": ["cat", "dog"]
        }, self.user)
        self.patient_id = str(self.patient.pk)
        
        # Create doctor
        self.role = create_role("temp_role", self.user)
        self.doctor = create_doctor({
            "name": "Doctor",
            "phoneNumber": "7809037033"
        }, self.user, self.role)
        self.doctor_id = str(self.doctor.pk)

        # Create template
        self.template = create_template(
            {
                "name": "Dentist",
                "medicalHistoryColumns": {
                    "Tien su toan than": "TEXT",
                    "Tien su rang ham mat": "TEXT"
                },
                "observationColumns": {
                    "Trieu chung ngoai mieng": "TEXT",
                    "Trieu chung trong rang": "IMAGE"
                },
                "treatmentColumns": {
                    "treatmentType": "TEXT",
                }
            }, self.user
        )

        # Create record
        self.record = create_record({
            "reasonForVisit": "Dau rang",
            "symptom": "Dau rang ve dem, khong ngu duoc",
            "medicalHistory": {
                "Tien su toan than": "Sau rang co lon, da tung tram va theo doi tuy rang 1 nam truoc",
                "Tien su rang ham mat": "Mat rang do nha chu"
            },
            "vitalSigns": {
                "heartRate": 90,
                "temperature": 37,
                "breathRate": 18,
                "bloodPressure": "120/80 mmHg"
            },
            "observations": {
                "Trieu chung ngoai mieng": [
                    "Sung ma trai"
                ],
                "Trieu chung trong rang": [
                    "R0lGODlhAQABAIAAAAUEBAAAACwAAAAAAQABAAACAkQBADs="
                ]
            },
            "diagnosis": "Viem tuy cap rang 25",
            "treatmentPlan": [
                "Noi nha rang 25",
                "Phuc hinh mao rang 25",
                "Cao voi rang"
            ]            
        }, self.patient, self.template, self.doctor)
        self.record_id = str(self.record.record_id)

        # Create treatment
        self.treatment = create_treatment({
            "treatmentType": "cao voi rang"
        }, self.record, self.template)
        self.treatment_id = str(self.treatment.pk)

    
    def test_get_treatment_should_return_200(self):
        response = self.client.get(f"/service/user/{self.user_id}/patients/{self.patient_id}/records/{self.record_id}/treatments/{self.treatment_id}/")
        self.assertEqual(response.status_code, 200)


    def test_get_treatment_not_belong_to_record_should_return_400(self):
        record = create_record({
            "reasonForVisit": "Dau rang",
            "symptom": "Dau rang ve dem, khong ngu duoc",
            "medicalHistory": {
                "Tien su toan than": "Sau rang co lon, da tung tram va theo doi tuy rang 1 nam truoc",
                "Tien su rang ham mat": "Mat rang do nha chu"
            },
            "vitalSigns": {
                "heartRate": 90,
                "temperature": 37,
                "breathRate": 18,
                "bloodPressure": "120/80 mmHg"
            },
            "observations": {
                "Trieu chung ngoai mieng": [
                    "Sung ma trai"
                ],
                "Trieu chung trong rang": [
                    "R0lGODlhAQABAIAAAAUEBAAAACwAAAAAAQABAAACAkQBADs="
                ]
            },
            "diagnosis": "Viem tuy cap rang 25",
            "treatmentPlan": [
                "Noi nha rang 25",
                "Phuc hinh mao rang 25",
                "Cao voi rang"
            ]            
        }, self.patient, self.template, self.doctor)
        record_id = str(record.record_id)

        response = self.client.get(f"/service/user/{self.user_id}/patients/{self.patient_id}/records/{record_id}/treatments/{self.treatment_id}/")
        self.assertEqual(response.status_code, 400)


    def test_get_non_existed_treatment_should_return_404(self):
        response = self.client.get(f"/service/user/{self.user_id}/patients/{self.patient_id}/records/{self.record_id}/treatments/{uuid.uuid4()}/")
        self.assertEqual(response.status_code, 404)