from django.test import TestCase
from rest_framework.test import APIClient
from ..test_utils import *
import uuid


# THINGS TO TEST
# test create patient -> 201
# test create patient with missing keys -> 400
# test create duplicated patient -> 400
# test get single patient -> 200
# test update patient -> 201
# test update patient with missing keys -> 400
# test get all patients -> 200


class PatientServiceTest(TestCase):

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

    
    def test_create_patient_should_return_201(self):
        patient_data = {
            "name": "patient1",
            "gender": "M",
            "address": "281/24 lvs",
            "dateOfBirth": "1999-12-02",
            "phoneNumber": "+8454897822",
            "note": "VIP",
            "allergies": ["cat", "dog"]
        }
        response = self.client.post(f"/service/user/{self.user_id}/patients/", patient_data, format='json')
        self.assertEqual(response.status_code, 201)

    
    def test_create_patient_with_missing_keys_should_return_400(self):
        patient_data = {
            "name": "patient1",
            "gender": "M",
            "address": "281/24 lvs",
            "dateOfBirth": "1999-12-02",
            "note": "VIP",
        }
        response = self.client.post(f"/service/user/{self.user_id}/patients/", patient_data, format='json')
        self.assertEqual(response.status_code, 400)

    
    def test_create_duplicate_patient_should_return_400(self):
        patient_data = {
            "name": "patient",
            "gender": "M",
            "address": "281/24 lvs",
            "dateOfBirth": "1999-12-02",
            "phoneNumber": "+8454897822",
            "note": "VIP",
            "allergies": ["cat", "dog"]
        }
        response = self.client.post(f"/service/user/{self.user_id}/patients/", patient_data, format='json')
        self.assertEqual(response.status_code, 400)

    
    def test_get_single_patient_should_return_200(self):
        response = self.client.get(f"/service/user/{self.user_id}/patients/{self.patient_id}/")
        self.assertEqual(response.status_code, 200)

    
    def test_update_patient_should_return_201(self):
        patient_data = {
            "name": "patient",
            "gender": "M",
            "address": "281/24 lvs",
            "dateOfBirth": "1999-12-03",
            "phoneNumber": "+8454897822",
            "note": "VIP",
            "allergies": ["cat", "dog"]
        }
        response = self.client.patch(f"/service/user/{self.user_id}/patients/{self.patient_id}/", patient_data, format='json')
        self.assertEqual(response.status_code, 201)

        # Check if updated data reflected
        data = response.data["metadata"]
        self.assertEqual(data["dateOfBirth"], patient_data["dateOfBirth"])


    def test_update_patient_with_missing_keys_should_return_400(self):
        patient_data = {
            "name": "patient",
            "gender": "M",
            "address": "281/24 lvs",
            "phoneNumber": "+8454897822",
            "note": "VIP",
            "allergies": ["cat", "dog"]
        }
        response = self.client.patch(f"/service/user/{self.user_id}/patients/{self.patient_id}/", patient_data, format='json')
        self.assertEqual(response.status_code, 400)


    def test_get_all_patients_should_return_200(self):
        response = self.client.get(f"/service/user/{self.user_id}/patients/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["metadata"]), 1)