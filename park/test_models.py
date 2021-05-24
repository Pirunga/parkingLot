from django.test import TestCase
from datetime import datetime, timezone, timedelta
from park.models import Level, Princing, Vehicle, Space
from model_bakery import baker


class LevelModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.level = Level.objects.create(
            name="floor 77",
            fill_priority=1,
            motorcycle_spaces=10,
            car_spaces=10,
        )

    def test_information_fields(self) -> None:
        self.assertIsInstance(self.level.name, str)
        self.assertIsInstance(self.level.fill_priority, int)
        self.assertIsInstance(self.level.motorcycle_spaces, int)
        self.assertIsInstance(self.level.car_spaces, int)


class PricingModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.pricing = Princing.objects.create(a_coefficient=100, b_coefficient=100)

    def test_information_fields(self) -> None:
        self.assertIsInstance(self.pricing.a_coefficient, int)
        self.assertIsInstance(self.pricing.b_coefficient, int)


class VehicleModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.vehicle = Vehicle.objects.create(
            vehicle_type="car",
            license_plate="HTO2127",
            arrived_at=datetime.now(timezone(offset=-timedelta(hours=3))),
            paid_at=datetime.now(timezone(offset=-timedelta(hours=1))),
            amount_paid=0,
            level=Level.objects.create(
                name="floor 77",
                fill_priority=1,
                motorcycle_spaces=10,
                car_spaces=10,
            ),
        )

    def test_information_fields(self) -> None:
        self.assertIsInstance(self.vehicle.vehicle_type, str)
        self.assertIsInstance(self.vehicle.license_plate, str)
        self.assertIsInstance(self.vehicle.arrived_at, datetime)
        self.assertIsInstance(self.vehicle.paid_at, datetime)
        self.assertIsInstance(self.vehicle.amount_paid, int)


class SpaceModelTest(TestCase):
    def setUp(self) -> None:
        self.history = baker.make("park.Space")
