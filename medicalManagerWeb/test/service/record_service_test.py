from django.test import TestCase
from rest_framework.test import APIClient
from ..test_utils import *
from ...utils.formatter import *
import uuid


# THINGS TO TEST
# test create record -> 201
# test create record with missing keys -> 400
# test create record with non existed doctor -> 404
# test create record with doctor not belong to user -> 400
# test create record with non existed template -> 400
# test create record with template not belong to user -> 400
# test create record with mismatched template -> 400
# test update record -> 201
# test update record with missing keys -> 400
# test update record with non existed doctor -> 404
# test update record with doctor not belong to user -> 400
# test update record with non existed template -> 400
# test update record with template not belong to user -> 400
# test update record with mismatched template -> 400
# test get record -> 200
# test update and get record by version -> 200
# test get all records -> 200
# test get all records should return latest versions -> 200

RECORD_DATA = {
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
    "observation": {
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
}


class RecordServiceTest(TestCase):

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
            "phoneNumber": "+84854897822",
            "note": "VIP",
            "allergies": ["cat", "dog"]
        }, self.user)
        self.patient_id = str(self.patient.pk)
        
        # Create doctor
        self.role = create_role("temp_role", self.user)
        self.doctor = create_doctor({
            "name": "Doctor",
            "phoneNumber": "+17809037033"
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
                    "An extra column": "TEXT"
                }
            }, self.user
        )

        # Create record
        self.record = create_record(RECORD_DATA, self.patient, self.template, self.doctor)
        self.record_id = str(self.record.pk)

    
    def test_create_record_should_return_201(self):
        record_data = RECORD_DATA.copy()
        record_data["primary_doctor_id"] = self.doctor.pk
        record_data["template_id"] = self.template.pk
        response = self.client.post(f"/service/user/{self.user_id}/patients/{self.patient_id}/records/", record_data, format='json')
        self.assertEqual(response.status_code, 201)

    
    def test_create_record_with_missing_keys_should_return_400(self):
        record_data = {}
        response = self.client.post(f"/service/user/{self.user_id}/patients/{self.patient_id}/records/", record_data, format='json')
        self.assertEqual(response.status_code, 400)


    def test_create_record_with_non_existed_doctor_should_return_400(self):
        record_data = RECORD_DATA.copy()
        record_data["primary_doctor_id"] = uuid.uuid4()
        record_data["template_id"] = self.template.pk
        response = self.client.post(f"/service/user/{self.user_id}/patients/{self.patient_id}/records/", record_data, format='json')
        self.assertEqual(response.status_code, 400)


    def test_create_record_with_doctor_not_belong_to_user_should_return_400(self):
        new_user = create_user({
            "username": "user2",
            "password": "password1",
            "displayName": "User 2",
            "email": "user@gmail.com"
        })["user"]
        new_doctor = create_doctor({
            "name": "Doctor1",
            "phoneNumber": "+17809037033"
        }, new_user, self.role)
        record_data = RECORD_DATA.copy()
        record_data["primary_doctor_id"] = new_doctor.pk
        record_data["template_id"] = self.template.pk

        response = self.client.post(f"/service/user/{self.user_id}/patients/{self.patient_id}/records/", record_data, format='json')
        self.assertEqual(response.status_code, 400)


    def test_create_record_with_non_existed_template_should_return_400(self):
        record_data = RECORD_DATA.copy()
        record_data["primary_doctor_id"] = self.doctor.pk
        record_data["template_id"] = uuid.uuid4()
        response = self.client.post(f"/service/user/{self.user_id}/patients/{self.patient_id}/records/", record_data, format='json')
        self.assertEqual(response.status_code, 400)

    
    def test_create_record_with_template_not_belong_user_should_return_400(self):
        new_user = create_user({
            "username": "user2",
            "password": "password1",
            "displayName": "User 2",
            "email": "user@gmail.com"
        })["user"]
        new_template = create_template({
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
                "An extra column": "TEXT"
            }
        }, new_user)
        record_data = RECORD_DATA.copy()
        record_data["primary_doctor_id"] = self.doctor.pk
        record_data["template_id"] = new_template.pk

        response = self.client.post(f"/service/user/{self.user_id}/patients/{self.patient_id}/records/", record_data, format='json')
        self.assertEqual(response.status_code, 400)


    def test_create_record_with_mismatch_template_should_return_400(self):
        record_data = RECORD_DATA.copy()
        record_data["primary_doctor_id"] = self.doctor.pk
        record_data["template_id"] = self.template.pk
        record_data["observation"] = {
            "Trieu chung ngoai mienggg": [
                "Sung ma trai"
            ],
            "Trieu chung trong ranggg": [
                "R0lGODlhAQABAIAAAAUEBAAAACwAAAAAAQABAAACAkQBADs="
            ]
        }
    
        response = self.client.post(f"/service/user/{self.user_id}/patients/{self.patient_id}/records/", record_data, format='json')
        self.assertEqual(response.status_code, 400)

    
    def test_update_record_should_return_201(self):
        record_data = RECORD_DATA.copy()
        record_data["primary_doctor_id"] = self.doctor.pk
        record_data["template_id"] = self.template.pk
        record_data["symptom"] = "Dau mieng"
        response = self.client.patch(f"/service/user/{self.user_id}/patients/{self.patient_id}/records/{self.record_id}/", record_data, format='json')
        self.assertEqual(response.status_code, 201)
        parsed_response_data = json.loads(response.content)["metadata"]
        self.assertTrue(is_equal_fields(parsed_response_data, record_data, ["symptom"]))


    def test_update_record_with_missing_keys_should_return_400(self):
        record_data = {}
        response = self.client.patch(f"/service/user/{self.user_id}/patients/{self.patient_id}/records/{self.record_id}/", record_data, format='json')
        self.assertEqual(response.status_code, 400)

    
    def test_update_record_with_non_existed_doctor_should_return_400(self):
        record_data = RECORD_DATA.copy()
        record_data["primary_doctor_id"] = uuid.uuid4()
        record_data["template_id"] = self.template.pk
        response = self.client.patch(f"/service/user/{self.user_id}/patients/{self.patient_id}/records/{self.record_id}/", record_data, format='json')
        self.assertEqual(response.status_code, 400)


    def test_update_record_with_doctor_not_belong_to_user_should_return_400(self):
        new_user = create_user({
            "username": "user2",
            "password": "password1",
            "displayName": "User 2",
            "email": "user@gmail.com"
        })["user"]
        new_doctor = create_doctor({
            "name": "Doctor1",
            "phoneNumber": "+17809037033"
        }, new_user, self.role)
        record_data = RECORD_DATA.copy()
        record_data["primary_doctor_id"] = new_doctor.pk
        record_data["template_id"] = self.template.pk

        response = self.client.patch(f"/service/user/{self.user_id}/patients/{self.patient_id}/records/{self.record_id}/", record_data, format='json')
        self.assertEqual(response.status_code, 400)

    
    def test_update_record_with_non_existed_template_should_return_400(self):
        record_data = RECORD_DATA.copy()
        record_data["primary_doctor_id"] = self.doctor.pk
        record_data["template_id"] = uuid.uuid4()
        response = self.client.patch(f"/service/user/{self.user_id}/patients/{self.patient_id}/records/{self.record_id}/", record_data, format='json')
        self.assertEqual(response.status_code, 400)

    
    def test_update_record_with_template_not_belong_user_should_return_400(self):
        new_user = create_user({
            "username": "user2",
            "password": "password1",
            "displayName": "User 2",
            "email": "user@gmail.com"
        })["user"]
        new_template = create_template({
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
                "An extra column": "TEXT"
            }
        }, new_user)
        record_data = RECORD_DATA.copy()
        record_data["primary_doctor_id"] = self.doctor.pk
        record_data["template_id"] = new_template.pk
        response = self.client.patch(f"/service/user/{self.user_id}/patients/{self.patient_id}/records/{self.record_id}/", record_data, format='json')
        self.assertEqual(response.status_code, 400)


    def test_update_record_with_mismatch_template_should_return_400(self):
        record_data = RECORD_DATA.copy()
        record_data["primary_doctor_id"] = self.doctor.pk
        record_data["template_id"] = self.template.pk
        record_data["observation"] = {
            "Trieu chung ngoai mienggg": [
                "Sung ma trai"
            ],
            "Trieu chung trong ranggg": [
                "R0lGODlhAQABAIAAAAUEBAAAACwAAAAAAQABAAACAkQBADs="
            ]
        }
    
        response = self.client.patch(f"/service/user/{self.user_id}/patients/{self.patient_id}/records/{self.record_id}/", record_data, format='json')
        self.assertEqual(response.status_code, 400)


    def test_get_record_should_return_200(self):
        response = self.client.get(f"/service/user/{self.user_id}/patients/{self.patient_id}/records/{self.record_id}/")
        self.assertEqual(response.status_code, 200)
        parsed_response_data = json.loads(response.content)["metadata"]
        self.assertTrue(is_equal_fields(parsed_response_data, RECORD_DATA, ["symptom", "reasonForVisit", "diagnosis"]))

    
    def test_get_all_records_should_return_200(self):
        response = self.client.get(f"/service/user/{self.user_id}/patients/{self.patient_id}/records/")
        response_data = response.data["metadata"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), 1)