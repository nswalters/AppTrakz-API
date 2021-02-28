import json
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class RegisterTests(APITestCase):
    def setUp(self) -> None:
        pass

    def test_register_user(self):
        """
        Register a user
        """

        url = "/register"
        data = {
            "username": "testuser",
            "email": "testuser@test.com",
            "password": "testpassword",
            "first_name": "test",
            "last_name": "user"
        }
        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", json_response)
        self.assertIn("id", json_response)
        self.assertEqual(json_response["id"], 1)

    def test_login_user(self):
        """
        Login a user
        """

        # Register the user
        self.test_register_user()

        url = "/login"
        data = {
            "username": "testuser",
            "password": "testpassword"
        }
        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(json_response["valid"], True)
        self.assertEqual(json_response["id"], 1)
        self.assertIn("token", json_response)

    def test_login_user_failure(self):
        """
        Verify bad credentials are not accepted (returns "valid = false")
        """

        # Register a user
        self.test_register_user()

        url = "/login"
        data = {
            "username": "testuser",
            "password": "badpassword"
        }
        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(json_response["valid"], False)
