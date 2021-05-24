from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    is_superuser = serializers.BooleanField(required=True)
    is_staff = serializers.BooleanField(required=True)


class LevelSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    motorcycle_spaces = serializers.IntegerField(write_only=True)
    car_spaces = serializers.IntegerField(write_only=True)
    fill_priority = serializers.IntegerField()
    available_spaces = serializers.SerializerMethodField(read_only=True)

    def get_available_spaces(self, level):
        motorcycle_spaces = level.motorcycle_spaces
        car_spaces = level.car_spaces

        return {
            "available_motorcycle_spaces": motorcycle_spaces,
            "available_car_spaces": car_spaces,
        }


class PrincingsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    a_coefficient = serializers.IntegerField()
    b_coefficient = serializers.IntegerField()


class SpaceSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True, required=False)
    variety = serializers.CharField(required=False)
    level_name = serializers.CharField(required=False)


class VehiclesSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    license_plate = serializers.CharField()
    vehicle_type = serializers.CharField(required=False)
    arrived_at = serializers.DateTimeField(required=False)
    paid_at = serializers.DateTimeField(required=False)
    amount_paid = serializers.IntegerField(required=False)
    space = SpaceSerializer(required=False, default=None)
