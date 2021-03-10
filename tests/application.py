from django.contrib.auth.models import User
import json
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from apptrakzapi.models import Company, Status


class ApplicationTests(APITestCase):
    def setUp(self) -> None:
        """
        Configure initial requirements for Company Tests
        """

        # Create our user
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

        # Create the job to apply to
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

        # Create our initial 'Applied' status
        new_status = Status.objects.create(name='Applied')
        new_status.save()

        # Create a secondary status to verify updates
        second_status = Status.objects.create(name='Did not Move On')
        second_status.save()

    def test_create_new_job_application(self):
        """
        Verify we can create a new job application.
        """
        url = "/applications"
        data = {
            "job": 1
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["id"], 1)
        self.assertEqual(json_response["statuses"][0]["id"], 1)
        self.assertEqual(json_response["statuses"][0]["name"], "Applied")
        self.assertEqual(json_response["job"]["id"], 1)
        self.assertEqual(json_response["job"]["role_title"], "TestRole")

    def test_update_job_application(self):
        """
        Verify we can update a job application.
        """

        self.test_create_new_job_application()

        url = "/applications/1"
        data = {
            "is_active": False,
            "status": 2,
            "reason": "None Given"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(url, data, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["id"], 1)
        self.assertEqual(json_response["statuses"][0]["id"], 1)
        self.assertEqual(json_response["statuses"][0]["name"], "Applied")
        self.assertEqual(json_response["statuses"][1]["id"], 2)
        self.assertEqual(json_response["statuses"]
                         [1]["name"], "Did not Move On")
        self.assertEqual(json_response["job"]["id"], 1)
        self.assertEqual(json_response["job"]["role_title"], "TestRole")
