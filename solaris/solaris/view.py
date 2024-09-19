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

class AuthApiViewSet(viewsets.ModelViewSet):
    """Авторизация пользователей администратором"""
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny, IsAuthenticated]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    
class FeedbackFormApiView(viewsets.ModelViewSet):
    """Логика создания feedback формы"""

    queryset = FeedbackForm.objects.all()
    serializer_class = FeedbackSerializer
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
class SchoolApiView(viewsets.ModelViewSet):
    """Логика создания модели пользователя в рамках проекта"""
    queryset = SchoolUser.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    