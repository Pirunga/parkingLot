from django.contrib.auth import models
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from park.serializers import (
    UserSerializer,
    LevelSerializer,
    PrincingsSerializer,
    VehiclesSerializer,
)
from datetime import datetime, timezone, timedelta

from park.models import Level, Princing, Vehicle, Space


class UserView(APIView):
    def post(self, request):
        data = request.data

        serializer = UserSerializer(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=data["username"])

            return Response(status=status.HTTP_409_CONFLICT)

        except User.DoesNotExist:
            user = User.objects.create_user(**data)

            serializer = UserSerializer(user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)


class LevelsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        level = Level.objects.create(**data)

        serializer = LevelSerializer(level)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        all_levels = [LevelSerializer(level).data for level in Level.objects.all()]

        return Response(all_levels, status=status.HTTP_200_OK)


class PricingView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        serializer = PrincingsSerializer(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        prices = Princing.objects.create(**serializer.data)

        serializer = PrincingsSerializer(prices)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VehicleView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        serializer = VehiclesSerializer(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if not Princing.objects.all():
            return Response(status=status.HTTP_404_NOT_FOUND)

        all_levels = [level for level in Level.objects.all().order_by("fill_priority")]

        if not all_levels:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if data["vehicle_type"] == "car":
            car_spaces = [level for level in all_levels if level.car_spaces > 0]

            if not car_spaces:
                return Response(status=status.HTTP_404_NOT_FOUND)

            level = Level.objects.get(id=car_spaces[0].id)

            level.car_spaces -= 1

            level.save()

        if data["vehicle_type"] == "motorcycle":
            motorcycle_spaces = [
                level for level in all_levels if level.motorcycle_spaces > 0
            ]

            if not motorcycle_spaces:
                return Response(status=status.HTTP_404_NOT_FOUND)

            level = Level.objects.get(id=motorcycle_spaces[0].id)

            level.motorcycle_spaces -= 1

            level.save()

        arrived = datetime.now(timezone(offset=-timedelta(hours=3)))

        vehicle = Vehicle.objects.create(
            arrived_at=arrived,
            level=level,
            **serializer.data,
        )

        vehicle.save()

        space = Space.objects.create(level=level, vehicle=vehicle)

        space.level_name = level.name

        space.variety = vehicle.vehicle_type

        vehicle.space = space

        serializer = VehiclesSerializer(vehicle)

        return Response(serializer.data, status.HTTP_201_CREATED)


class VehiclePaymentView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, vehicle_id):
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)

        level = Level.objects.get(id=vehicle.level_id)

        if vehicle.vehicle_type == "car":
            level.car_spaces += 1

        if vehicle.vehicle_type == "motorcycle":
            level.motorcycle_spaces += 1

        level.save()

        coefficient = Princing.objects.last()

        a_coefficient = coefficient.a_coefficient

        b_coefficient = coefficient.b_coefficient

        vehicle.paid_at = datetime.now(timezone(offset=-timedelta(hours=3)))

        difference_time = vehicle.paid_at - vehicle.arrived_at

        hour = difference_time.total_seconds() / 3600

        vehicle.amount_paid = a_coefficient + b_coefficient * hour

        vehicle.space = None

        vehicle.save()

        serializer = VehiclesSerializer(vehicle)

        return Response(serializer.data, status=status.HTTP_200_OK)
