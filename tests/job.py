# from django.contrib.auth.models import User
import json
from rest_framework import status
# from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from apptrakzapi.models import Job


class JobTests(APITestCase):
    def setUp(self) -> None:
        """
        Configure initial requirements for Company Tests
        """
        # create our user
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
        self.userID = json_response["id"]

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # create a company to add the job to
        url = "/companies"
        data = {
            "name": "TestCompany",
            "address1": "1234 Test St",
            "address2": "suite 999",
            "city": "Testing",
            "state": "TG",
            "zipcode": 12345,
            "website": "https://www.test.com"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_job(self):
        """
        Verify we can create a job via the API
        """

        url = "/jobs"
        data = {
            "company": 1,
            "role_title": "TestRole",
            "type": "Test",
            "qualifications": "TestQuals",
            "post_link": "https://www.testpostlink.com",
            "salary": None,
            "description": "Just a test to create a job."
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["id"], 1)
        self.assertEqual(json_response["role_title"], "TestRole")
