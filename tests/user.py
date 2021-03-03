import json
from rest_framework import status
from rest_framework.test import APITestCase


class UserTests(APITestCase):
    def setUp(self) -> None:
        """
        Create a new account
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
        self.token = json_response["token"]

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_profile_user_exists(self):
        """
        Verify a user can view their profile details
        """
        url = "/user/profile"
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url, None, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["id"], 1)

    def test_update_user_profile(self):
        """
        Verify a user can update their profile
        """
        url = "/user/profile"
        data = {
            "bio": "This is a test bio",
            "profile_image": None
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        url = "/user/profile"
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url, None, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["id"], 1)
        self.assertEqual(json_response["bio"], "This is a test bio")
