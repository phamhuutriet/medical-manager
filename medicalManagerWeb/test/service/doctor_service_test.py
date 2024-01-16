from django.test import TestCase
from rest_framework.test import APIClient
from ..test_utils import *
import uuid


# THINGS TO TEST
# test create doctor -> return 201
# test create doctor missing key -> return 400
# test create doctor missing role -> return 400
# test create duplicated doctor -> return 400
# test update doctor -> return 201
# test update doctor missing key -> return 400
# test update doctor missing role -> return 400
# test get all doctors -> return 200
# test get single doctor -> return 200

DOCTOR_DATA = {
    "name": "Doctor",
    "phoneNumber": "7809037033"
}


class TestDoctorService(TestCase):

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
        self.doctor = create_doctor(DOCTOR_DATA, self.user, self.role)
        self.doctor_id = str(self.doctor.pk)

    
    def test_create_doctor_should_return_201(self):
        doctor_data = {
            "name": "Doctor1",
            "phoneNumber": "+17809037033",
            "role_id": self.role.pk
        }
        response = self.client.post(f"/service/user/{self.user_id}/doctors/", doctor_data, format='json')
        # Only in test, to make it use the camelCaseConverter renderer
        self.assertEqual(response.status_code, 201)
        parsed_response_data = json.loads(response.content)["metadata"]
        self.assertTrue(is_equal_fields(parsed_response_data, doctor_data, ["name", "phoneNumber"]))

    
    def test_create_doctor_missing_key_should_return_400(self):
        doctor_data = {
            "name": "Doctor1",
            "phoneNumber": "+17809037033",
        }
        response = self.client.post(f"/service/user/{self.user_id}/doctors/", doctor_data, format='json')
        self.assertEqual(response.status_code, 400)


    def test_create_doctor_non_existed_role_should_return_400(self):
        random_uuid = uuid.uuid4()
        doctor_data = {
            "name": "Doctor1",
            "phoneNumber": "+17809037033",
            "role": {
                "id": str(random_uuid),
                "name": self.role.name
            }
        }
        response = self.client.post(f"/service/user/{self.user_id}/doctors/", doctor_data, format='json')
        self.assertEqual(response.status_code, 400)


    def test_create_duplicated_doctor_should_return_400(self):
        doctor_data = {
            "name": "Doctor",
            "phoneNumber": "+17809037033",
            "role": {
                "id": str(self.role.pk),
                "name": self.role.name
            }
        }
        response = self.client.post(f"/service/user/{self.user_id}/doctors/", doctor_data, format='json')
        self.assertEqual(response.status_code, 400)


    def test_update_doctor_missing_key_should_return_400(self):
        doctor_data = {
            "name": "Doctor1",
            "phoneNumber": "+17809037033",
        }
        response = self.client.patch(f"/service/user/{self.user_id}/doctors/{self.doctor_id}/", doctor_data, format='json')
        self.assertEqual(response.status_code, 400)


    def test_update_doctor_non_existed_role_should_return_400(self):
        doctor_data = {
            "name": "Doctor1",
            "phoneNumber": "+17809037033",
            "role_id": uuid.uuid4()
        }
        response = self.client.patch(f"/service/user/{self.user_id}/doctors/{self.doctor_id}/", doctor_data, format='json')
        self.assertEqual(response.status_code, 400)


    def test_update_doctor_should_return_201(self):
        doctor_data = {
            "name": "Doctor1",
            "phoneNumber": "+17809037033",
            "role_id": self.role.pk
        }
        response = self.client.patch(f"/service/user/{self.user_id}/doctors/{self.doctor_id}/", doctor_data, format='json')
        self.assertEqual(response.status_code, 201)
        parsed_response_data = json.loads(response.content)["metadata"]
        self.assertTrue(is_equal_fields(parsed_response_data, doctor_data, ["name", "phoneNumber"]))


    def test_get_all_doctors_should_return_200(self):
        response = self.client.get(f"/service/user/{self.user_id}/doctors/")
        self.assertEqual(response.status_code, 200)


    def test_get_single_doctor_should_return_200(self):
        response = self.client.get(f"/service/user/{self.user_id}/doctors/{self.doctor_id}/")
        self.assertEqual(response.status_code, 200)
        parsed_response_data = json.loads(response.content)["metadata"]
        self.assertTrue(is_equal_fields(parsed_response_data, DOCTOR_DATA, ["name", "phoneNumber"]))