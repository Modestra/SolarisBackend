from rest_framework import (status, viewsets)
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from solaris.serializers import *

class RegisterApiView(APIView):
    """Регистрация ученика со стороны администратора"""
    def post(self, request):
        serializers = AdminUserSerializer(data=request.data)
        if serializers.is_valid():
            user = serializers.save()
            refresh = RefreshToken.for_user(user)

            refresh.payload.update({
                "login": user.login,
                "password": user.password
            })

            return Response({"refresh": str(refresh), "access": str(refresh.access_token)}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Невалидная форма записи"}, status=status.HTTP_403_FORBIDDEN)

class LoginApiView(APIView):

    def post(self, request):

        serializers = UserSerializer(data=request.data)

        if serializers.is_valid():
            return Response(serializers.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Некорректно введены данные"}, status=status.HTTP_403_FORBIDDEN)