from rest_framework import serializers


class CredencialSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
