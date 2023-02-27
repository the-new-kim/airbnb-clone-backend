from django.urls import reverse
from rest_framework.test import APITestCase
from users.models import User


class TestAmenities(APITestCase):
    USERNAME = "testuser"
    PASSWORD = "1111"

    URL = "/api/v1/rooms/amenities"

    # def setUp(self):
    #     user = User.objects.create(username=self.USERNAME, password=self.PASSWORD)
    #     print("USER:::::", user)

    def test_all_amenites(self):
        # user_data = {
        #     "username": self.USERNAME,
        #     "password": self.PASSWORD,
        # }

        # jwt_response = self.client.post("/api/v1/users/jwt-login", user_data)
        # print("JWT RESPONSE::::", jwt_response)

        response = self.client.get(self.URL)
        print("RESPONSE::::", response)

        # print("RESPONSE:::::", response)
        # self.assertEqual(
        #     response.status_code,
        #     200,
        #     "Status code is not 200",
        # )
