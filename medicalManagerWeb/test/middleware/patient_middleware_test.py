from django.test import TestCase
from rest_framework.test import APIClient
from ..test_utils import *
import uuid


# THINGS TO TEST
# get patient not belong to user -> 400
# get patient belong to a user -> 200
# get not existed patient -> 404


class PatientMiddlewareTest(TestCase):

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
        
    
    def test_patient_not_belong_to_user_should_return_400(self):
        user_data = {
            "username": "user2",
            "password": "password1",
            "displayName": "User 2",
            "email": "user@gmail.com"
        }
        user_id = str(create_user(user_data)["user"].pk)
        response = self.client.get(f"/service/user/{user_id}/patients/{self.patient_id}/")
        self.assertEqual(response.status_code, 400)

    
    def test_patient_belong_to_user_should_return_200(self):
        response = self.client.get(f"/service/user/{self.user_id}/patients/{self.patient_id}/")
        self.assertEqual(response.status_code, 200)

    
    def test_non_existed_patient_should_return_404(self):
        random_uuid = uuid.uuid4()
        response = self.client.get(f"/service/user/{self.user_id}/patients/{random_uuid}/")
        self.assertEqual(response.status_code, 404)