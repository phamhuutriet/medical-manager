from django.test import TestCase
from rest_framework.test import APIClient
from ..test_utils import *


# THINGS TO TESTS
# test access -> no need auth
# test doctors -> need auth
# test patients -> need auth


class UserMiddlewareTest(TestCase):
    
    def setUp(self):
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
        
    
    def test_call_sign_in_should_return_200(self):
        response = self.client.post(f"/service/access/signin/", self.user_data)
        self.assertEqual(response.status_code, 200)

    def test_call_doctor_urls_without_credentails_should_return_401(self):
        response = self.client.get(f"/service/user/{self.user_id}/doctors/")
        self.assertEqual(response.status_code, 401)

    def test_call_doctor_urls_with_credentials_should_return_200(self):
        self.client.credentials(**self.user_headers)
        response = self.client.get(f"/service/user/{self.user_id}/doctors/")
        self.assertEqual(response.status_code, 200)

    def test_call_patients_urls_without_credentials_should_return_401(self):
        response = self.client.get(f"/service/user/{self.user_id}/patients/")
        self.assertEqual(response.status_code, 401)

    def test_call_patients_urls_with_credentials_should_return_200(self):
        self.client.credentials(**self.user_headers)
        response = self.client.get(f"/service/user/{self.user_id}/patients/")
        self.assertEqual(response.status_code, 200)