from django.contrib.auth.models import User
import json
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from apptrakzapi.models import Company


class CompanyTests(APITestCase):
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

        our_user = User.objects.get(pk=self.userID)

        # create a couple of companies for that user
        company1 = Company.objects.create(
            user=our_user,
            name="ZName1",
            address1="Address1_1",
            address2="Address2_1",
            city="City1",
            state="State1",
            zipcode="11111",
            website="Website1"
        )
        company1.save()

        company2 = Company.objects.create(
            user=our_user,
            name="Name2",
            address1="Address1_2",
            address2="Address2_2",
            city="City2",
            state="State2",
            zipcode="22222",
            website="Website2"
        )
        company2.save()

        # This company is 'deleted' and therefore shouldn't show up
        # when we query for a set of companies
        deleted_company = Company.objects.create(
            user=our_user,
            name="DeletedCompany",
            address1="Address1_3",
            address2="Address2_3",
            city="City3",
            state="State3",
            zipcode="33333",
            website="Website3"
        )
        deleted_company.save()
        deleted_company.delete()

    def test_get_list_user_companies(self):
        """
        Verify we can get all of a user's active companies in alphabetical order
        """

        url = "/companies"
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url, None, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json_response), 2)
        self.assertEqual(json_response[0]["id"], 2)
        self.assertEqual(json_response[0]['name'], "Name2")
        self.assertEqual(json_response[1]['id'], 1)
        self.assertEqual(json_response[1]['name'], "ZName1")

    def test_create_company(self):
        """
        Verify we can create a company via the API
        """

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
        self.assertEqual(json_response["id"], 4)
        self.assertEqual(json_response["name"], "TestCompany")
        self.assertEqual(json_response["zipcode"], 12345)

    def test_update_company(self):
        """
        Verify we can update a company via the API
        """

        self.test_create_company()

        url = "/companies/4"
        data = {
            "name": "UpdatedCompany",
            "address1": "1234 Test St",
            "address2": "suite 999",
            "city": "Testing",
            "state": "TG",
            "zipcode": 12345,
            "website": "https://www.test.com"
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(url, data, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["id"], 4)
        self.assertEqual(json_response["name"], "UpdatedCompany")
