from typing import Any
from rest_framework import (status, viewsets)
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.permissions import *
from rest_framework.authtoken.models import Token
from solaris.serializer import *
from solaris.mixin import *
from solaris.models import *
from solaris.permissions import *

class AuthApiViewSet(viewsets.ModelViewSet):
    """Авторизация пользователей для входа в приложение"""
    
    queryset = SchoolUser.objects.all()
    serializer_class = AuthSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializers = AuthSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            user = SchoolUser.objects.get(username=request.data["username"])
            return Response({"user": serializers.data, "token": user.token}, status=status.HTTP_200_OK)
        return Response({"user": "Ошибка"}, status=status.HTTP_403_FORBIDDEN)
    
class FeedbackFormApiView(viewsets.ModelViewSet):
    """Логика создания feedback формы"""

    queryset = FeedbackForm.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
class SchoolApiView(viewsets.ModelViewSet):
    """Логика создания модели пользователя в рамках проекта"""
    queryset = SchoolUser.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class RulesApiViewSet(viewsets.ModelViewSet):

    queryset = Rules.objects.all()
    serializer_class = RulesSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
class CompetitionApiViewSet(viewsets.ModelViewSet):

    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
class CompetitionFilesApiViewSet(viewsets.ModelViewSet):

    queryset = CompetitionFiles.objects.all()
    serializer_class =CompetitionFileSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class ShopApiViewSet(viewsets.ModelViewSet):

    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminUser]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


    