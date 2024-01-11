from django.test import TestCase
from rest_framework.test import APIClient
from ..test_utils import *
import uuid


# THINGS TO TEST
# test get template not belong to user -> 400
# test get non existed template -> 404
# test get template belong to user -> 200


class TemplateMiddlewareTest(TestCase):

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
        self.template_id = str(self.template.pk)

    
    def test_get_template_not_belong_to_user_should_return_400(self):
        new_user = create_user({
            "username": "user2",
            "password": "password1",
            "displayName": "User 2",
            "email": "user@gmail.com"
        })["user"]
        new_user_id = str(new_user.pk)

        response = self.client.get(f"/service/user/{new_user_id}/templates/{self.template_id}/")
        self.assertEqual(response.status_code, 400)

    
    def test_get_non_existed_template_should_return_404(self):
        response = self.client.get(f"/service/user/{self.user_id}/templates/{uuid.uuid4()}/")
        self.assertEqual(response.status_code, 404)

    
    def test_get_template_should_return_200(self):
        response = self.client.get(f"/service/user/{self.user_id}/templates/{self.template_id}/")
        self.assertEqual(response.status_code, 200)