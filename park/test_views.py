from django.http import response
from django.test import TestCase, client
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from datetime import datetime, timezone, timedelta


class TestLevelCreateGetView(TestCase):
    def setUp(self) -> None:
        admin_user_data = {
            "username": "admin",
            "password": "1234",
            "is_superuser": True,
            "is_staff": True,
        }

        self.viewer_user = User.objects.create_user(**admin_user_data)

        add_level_permission = Permission.objects.get(codename="add_level")
        add_pricing_perimission = Permission.objects.get(codename="add_princing")
        add_vehicle_perimission = Permission.objects.get(codename="add_vehicle")

        self.viewer_user.user_permissions.add(add_level_permission)
        self.viewer_user.user_permissions.add(add_pricing_perimission)
        self.viewer_user.user_permissions.add(add_vehicle_perimission)

        self.level_data = {
            "name": "floor 1",
            "fill_priority": 2,
            "motorcycle_spaces": 20,
            "car_spaces": 50,
        }

        self.level_created_data = {
            "id": 1,
            "name": "floor 1",
            "fill_priority": 2,
            "available_spaces": {
                "available_motorcycle_spaces": 20,
                "available_car_spaces": 50,
            },
        }

        self.pricing_data = {
            "a_coefficient": 100,
            "b_coefficient": 100,
        }

        self.pricing_created_data = {
            "id": 1,
            "a_coefficient": 100,
            "b_coefficient": 100,
        }

        self.vehicle_data = {
            "vehicle_type": "car",
            "license_plate": "AYO1029",
        }

        self.vehicle_created_data = {
            "id": 1,
            "license_plate": "AYO1029",
            "vehicle_type": "car",
            "arrived_at": datetime.now(timezone(offset=-timedelta(hours=3))),
            "paid_at": None,
            "amount_paid": None,
            "space": {
                "id": 1,
                "variety": "car",
                "level_name": "floor 1",
            },
        }

        self.vehicle_out_data = {
            "license_plate": "AYO1029",
            "vehicle_type": "car",
            "arrived_at": datetime.now(timezone(offset=-timedelta(hours=3))),
            "paid_at": datetime.now(timezone(offset=-timedelta(hours=3))),
            "amount_paid": 100,
            "space": None,
        }

    def test_logged_in_user_can_list_levels(self):
        client = APIClient()
        token = Token.objects.get_or_create(user=self.viewer_user)[0]
        client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        response = client.get("/api/levels/")
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertEqual(response_data, [])

    def test_can_only_list_levels_with_valid_token(self):
        client = APIClient()
        response = client.get("/api/levels/")
        self.assertEqual(response.status_code, 401)

    def test_looged_in_user_can_create_level(self):
        client = APIClient()
        token = Token.objects.get_or_create(user=self.viewer_user)[0]
        client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        response = client.post("/api/levels/", self.level_data, format="json")
        self.assertEqual(response.status_code, 201)

        response_data = response.json()
        self.assertEqual(response_data, self.level_created_data)

    def test_create_level_with_unvalid_token(self):
        client = APIClient()
        response = client.post("/api/levels/", self.level_data, format="json")
        self.assertEqual(response.status_code, 401)

    def test_create_pricing_with_valid_token(self):
        client = APIClient()
        token = Token.objects.get_or_create(user=self.viewer_user)[0]
        client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        response = client.post("/api/pricings/", self.pricing_data, format="json")
        self.assertEqual(response.status_code, 201)

        response_data = response.json()
        self.assertEqual(response_data, self.pricing_created_data)

    def test_create_princing_with_unvalid_token(self):
        client = APIClient()

        response = client.post("/api/pricings/", self.pricing_data, format="json")
        self.assertEqual(response.status_code, 401)

    def test_create_princing_with_unvalid_body(self):
        client = APIClient()
        token = Token.objects.get_or_create(user=self.viewer_user)[0]
        client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        response2 = client.post("/api/pricings/", {}, format="json")
        self.assertEqual(response2.status_code, 400)

    def test_create_vehicle_with_valid_token(self):
        client = APIClient()
        token = Token.objects.get_or_create(user=self.viewer_user)[0]
        client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        client.post("/api/pricings/", self.pricing_data, format="json")
        client.post("/api/levels/", self.level_data, format="json")

        response = client.post("/api/vehicles/", self.vehicle_data, format="json")
        self.assertEqual(response.status_code, 201)

        response_data = response.json()
        self.assertEqual(response_data, self.vehicle_created_data)

    def test_put_vehicle_with_valid_token(self):
        client = APIClient()
        token = Token.objects.get_or_create(user=self.viewer_user)[0]
        client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        client.post("/api/pricings/", self.pricing_data, format="json")
        client.post("/api/levels/", self.level_data, format="json")
        client.post("/api/vehicles/", self.vehicle_data, format="json")

        response = client.put("/api/vehicles/1")

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data, self.vehicle_out_data)
