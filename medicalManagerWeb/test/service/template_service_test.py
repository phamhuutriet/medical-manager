from django.test import TestCase
from rest_framework.test import APIClient
from ..test_utils import *
from ...utils.formatter import *
import uuid


# THINGS TO TEST
# test create template -> 201
# test create template with missing keys -> 400
# test create template with invalid column value type -> 400
# test create duplicate template -> 400
# test update template -> 201
# test update template with missing keys -> 400
# test update template with invalid column value type -> 400
# test get all templates -> 200


TEMPLATE_DATA = {
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
}


class TemplateServiceTest(TestCase):

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

        # Create template
        self.template = create_template(
            TEMPLATE_DATA, self.user
        )
        self.template_id = str(self.template.pk)

    
    def test_create_template_should_return_201(self):
        template_data = TEMPLATE_DATA.copy()
        template_data["name"] = "DENTIST"

        response = self.client.post(f"/service/user/{self.user_id}/templates/", template_data, format='json')
        self.assertEqual(response.status_code, 201)

    
    def test_create_template_with_missing_keys_should_return_400(self):
        template_data = {}
        response = self.client.post(f"/service/user/{self.user_id}/templates/", template_data, format='json')
        self.assertEqual(response.status_code, 400)

    
    def test_create_template_with_invalid_column_type_should_return_400(self):
        template_data = TEMPLATE_DATA.copy()
        template_data["observationColumns"] = {
            "Trieu chung ngoai mieng": "TEXTXX" # should be TEXT or IMAGE
        }
        response = self.client.post(f"/service/user/{self.user_id}/templates/", template_data, format='json')
        self.assertEqual(response.status_code, 400)


    def test_create_duplicate_template_should_return_400(self):
        response = self.client.post(f"/service/user/{self.user_id}/templates/", TEMPLATE_DATA, format='json')
        self.assertEqual(response.status_code, 400)

    
    def test_update_template_should_return_201(self):
        template_data = TEMPLATE_DATA.copy()
        template_data["name"] = "DENTIST"

        response = self.client.patch(f"/service/user/{self.user_id}/templates/{self.template_id}/", template_data, format='json')
        self.assertEqual(response.status_code, 201)

    
    def test_create_template_with_missing_keys_should_return_400(self):
        template_data = {}
        response = self.client.patch(f"/service/user/{self.user_id}/templates/{self.template_id}/", template_data, format='json')
        self.assertEqual(response.status_code, 400)

    
    def test_create_template_with_invalid_column_type_should_return_400(self):
        template_data = TEMPLATE_DATA.copy()
        template_data["observationColumns"] = {
            "Trieu chung ngoai mieng": "TEXTXX" # should be TEXT or IMAGE
        }
        response = self.client.patch(f"/service/user/{self.user_id}/templates/{self.template_id}/", template_data, format='json')
        self.assertEqual(response.status_code, 400)

    
    def test_get_all_templates_should_return_200(self):
        response = self.client.get(f"/service/user/{self.user_id}/templates/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["metadata"]), 1)