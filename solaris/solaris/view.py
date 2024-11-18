from typing import Any
from rest_framework import (status, viewsets, generics)
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
from solaris.authentication import SolarisJWTAuthentification

class AuthApiViewSet(ListViewSet):
    """Авторизация пользователей для входа в приложение"""
    
    queryset = SchoolUser.objects.all()
    serializer_class = AuthSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=["post"])
    def login(self, request, *args, **kwargs):
        serializers = AuthSerializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            return Response({"user": serializers.data}, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_403_FORBIDDEN)
    
class FeedbackFormApiView(viewsets.ModelViewSet):
    """Логика создания feedback формы"""

    queryset = FeedbackForm.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
class SchoolApiView(ListViewSet):
    """Логика создания модели пользователя в рамках проекта. Создавать может только пользователь, если он является администратором"""
    queryset = SchoolUser.objects.all()
    serializer_class = SchoolSerializer
    authentication_classes=[SolarisJWTAuthentification]
    permission_classes = [AllowAny, IsSchoolAdmin]

    def list(self, request, *args, **kwargs):
        """Вывести список всех пользователей"""
        return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=["post"], serializer_class=AdminUserSerializer)
    def create_user(self, request, *args, **kwargs):
        """Создает нового пользователя. Создавать пользователя может только администратор"""
        serializers = AdminUserSerializer(data=request.data)
        if serializers.is_valid():
            user = serializers.create(validated_data=request.data)
            return Response({"user": serializers.data, "token": user.token}, status=status.HTTP_201_CREATED)
        return Response({"error": "Некорректная форма передачи данных"}, status=status.HTTP_403_FORBIDDEN)
    
    @action(detail=False, methods=["post"], serializer_class=UserIdSerializer)
    def get_token(self, request):
        """Возвращает токен выбранного пользователя по user_id"""
        serializers = UserIdSerializer(data=request.data)
        pass

class RulesApiViewSet(CreateListViewSet):
    """Правила. Пока непонятно, что это, но пусть работает"""
    queryset = Rules.objects.all()
    serializer_class = RulesSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
class CompetitionApiViewSet(CreateListViewSet):

    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def add_files(self, request):
        serializers = CompetitionFileSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response({"error": "Некорректный запрос со стороны клиента"}, status=status.HTTP_403_FORBIDDEN)
            
class CompetitionFilesApiViewSet(CreateListViewSet):

    queryset = CompetitionFiles.objects.all()
    serializer_class = CompetitionFileSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class ShopApiViewSet(CreateListViewSet):

    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminUser]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


    