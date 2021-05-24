from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from authentication.serializers import CredencialSerializer


class LoginView(APIView):
    def post(self, request):
        data = request.data

        serializer = CredencialSerializer(data=data)

        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(
            username=data["username"], password=data["password"])

        if user:
            token = Token.objects.get_or_create(user=user)[0]
            return Response({"token": token.key}, status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
