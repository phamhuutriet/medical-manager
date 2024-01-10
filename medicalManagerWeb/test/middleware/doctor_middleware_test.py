from django.test import TestCase
from rest_framework.test import APIClient
from ..test_utils import *
import uuid

# THINGS TO TEST
# get doctor that not belong to user -> 400
# get doctor that belong to user -> 200
# get doctor that's not existed -> 404


class DoctorMiddlewareTest(TestCase):
    
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

        # Create doctor
        self.role = create_role("temp_role", self.user)
        self.doctor = create_doctor({
            "name": "Doctor",
            "phoneNumber": "7809037033"
        }, self.user, self.role)
        self.doctor_id = str(self.doctor.pk)

    
    def test_get_doctor_that_not_existed_should_return_404(self):
        random_uuid = uuid.uuid4()
        response = self.client.get(f"/service/user/{self.user_id}/doctors/{random_uuid}/")
        self.assertEqual(response.status_code, 404)


    def test_get_doctor_that_not_belong_to_selected_user_should_return_400(self):
        user_data = {
            "username": "user2",
            "password": "password1",
            "displayName": "User 2",
            "email": "user@gmail.com"
        }
        user_id = str(create_user(user_data)["user"].pk)
        response = self.client.get(f"/service/user/{user_id}/doctors/{self.doctor_id}/")
        self.assertEqual(response.status_code, 400)

    
    def test_get_doctor_that_belong_to_selected_user_should_return_200(self):
        response = self.client.get(f"/service/user/{self.user_id}/doctors/{self.doctor_id}/")
        self.assertEqual(response.status_code, 200)