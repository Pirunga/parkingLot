from django.db import models
from django.db.models.deletion import CASCADE


class Level(models.Model):
    name = models.CharField(max_length=255)
    fill_priority = models.IntegerField()
    motorcycle_spaces = models.IntegerField()
    car_spaces = models.IntegerField()


class Princing(models.Model):
    a_coefficient = models.IntegerField()
    b_coefficient = models.IntegerField()


class Space(models.Model):
    level = models.ForeignKey(Level, on_delete=CASCADE)


class Vehicle(models.Model):
    vehicle_type = models.CharField(max_length=50)
    license_plate = models.CharField(max_length=10)
    arrived_at = models.DateTimeField()
    paid_at = models.DateTimeField(null=True, blank=True, default=None)
    amount_paid = models.IntegerField(null=True, blank=True, default=None)
    level = models.ForeignKey(Level, on_delete=CASCADE)
    space = models.OneToOneField(Space, on_delete=CASCADE, null=True)
