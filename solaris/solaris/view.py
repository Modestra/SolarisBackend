from typing import Any
from rest_framework import (status, viewsets)
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from solaris.serializer import *
from solaris.mixin import *
from solaris.models import *

class AuthApiViewSet(viewsets.ModelViewSet):
    """Авторизация пользователей администратором"""
    
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
class FeedbackFormApiView(viewsets.ModelViewSet):
    """Логика создания feedback формы"""

    queryset = FeedbackForm.objects.all()
    serializer_class = FeedbackSerializer
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    