from typing import Any
import os
from rest_framework import (status, viewsets, generics)
from rest_framework.views import exception_handler
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.permissions import *
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser
from solaris.serializer import *
from solaris.mixin import *
from solaris.models import *
from solaris.permissions import *
from solaris.authentication import SolarisJWTAuthentification
from solaris.encoder import MessageEncoder
from drf_yasg.utils import swagger_auto_schema

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
            user = SchoolUser.objects.get(username=serializers.data["username"])
            if SchoolUser.objects.filter(username=serializers.data["username"]).exists():
                token = Token.objects.update(user_id=user.user_id, token=user.token, update_date=datetime.datetime.now())
            token = Token.objects.create(user_id=user.user_id, token=user.token)
            return Response({"user": serializers.data, "token": user.token}, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TokenApiView(ListViewSet):
    """Таблица токенов пользователей. Необходим для подтверждения авторизации. 
    Получить данные по токенам могут получить только авторизованные пользователи"""
    queryset = Token.objects.all()
    serializer_class = TokenSerializer
    authentication_classes = [SolarisJWTAuthentification]
    permission_classes = [AllowAny, IsSchoolAuthorized]

    def list(self, request, *args, **kwargs):
        """Получить список всех авторизованных пользователей"""
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(request_body=TokenSerializer, parser_classes=[MultiPartParser])
    @action(detail=False, methods=["put"], permission_classes=[IsSchoolAuthorized], parser_classes=[MultiPartParser])
    def refresh_token(self, request, *args):
        """Обновить токен пользователя, если у токена прошёл срок"""
        serializers = TokenSerializer(data=request.data)
        if serializers.is_valid():
            
            return Response({"token": serializers.data, "message": "Токен был обновлен"}, status=status.HTTP_200_OK)
        return Response({"message": "Некорректная форма передачи данных"}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=["post"], permission_classes=[IsSchoolAuthorized])
    def create_user_token(self, request):
        """Создать готовый токен по user_id"""
        serializers = TokenSerializer(data=request.data)
        if serializers.is_valid():
            user = SchoolUser.objects.get(user_id=serializers.data["user_id"])
            token = Token.objects.create(user_id=user.user_id, token=user.token, update_date=datetime.datetime.now())
            return Response({"user_id": token.user_id, "token": token.token}, status=status.HTTP_201_CREATED)
        return Response({"error": "Некорректная форма передачи данных"}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=["post"], serializer_class=TokenSerializer, permission_classes=[IsSchoolAuthorized])
    def get_user_token(self, request):
        """Получить токен по user_id"""
        serializers = TokenSerializer(data=request.data)
        if serializers.is_valid():
            user = SchoolUser.objects.get(user_id=serializers.data["user_id"])
            return Response({"user_id": user.user_id, "token": user.token}, status=status.HTTP_200_OK)
        return Response({"error": "Не удалось получить токен"}, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(request_body=TokenSerializer)
    @action(detail=False, methods=["delete"], serializer_class=TokenSerializer, permission_classes=[IsSchoolAuthorized])
    def delete_user_token(self, request):
        """Удалить токен по user_id"""
        serializers = TokenSerializer(data=request.data)
        if serializers.is_valid():
            token = Token.objects.filter(user_id=serializers.data["user_id"]).delete()
            return Response({"success": "Данные удалены"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Не удалось найти пользователя по данному user_id"}, status=status.HTTP_400_BAD_REQUEST)
    
class FeedbackFormApiView(viewsets.ModelViewSet):
    """Логика создания feedback формы"""

    queryset = FeedbackForm.objects.all()
    serializer_class = FeedbackSerializer
    authentication_classes=[SolarisJWTAuthentification]
    permission_classes = [IsSchoolAuthorized]
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
class SchoolApiView(ListViewSet):
    """Логика создания модели пользователя в рамках проекта. Создавать может только пользователь, если он является администратором"""
    queryset = SchoolUser.objects.all()
    serializer_class = SchoolSerializer
    authentication_classes=[SolarisJWTAuthentification]
    permission_classes = [AllowAny, IsSchoolAdmin, IsSchoolAuthorized]

    def list(self, request, *args, **kwargs):
        """Вывести список всех пользователей. Получить данные пользователей можно, если пользователь зарегестрирован и админ"""
        return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=["get"], permission_classes=[IsSchoolAuthorized])
    def current_user(self, request):
        """Получить user_id авторизированного пользователя"""
        user = SchoolUser.objects.get(user_id=request.user.user_id)
        return Response({"user_id": user.user_id}, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body=TokenSerializer)
    @action(detail=False, methods=["delete"], serializer_class=TokenSerializer, permission_classes=[IsSchoolAdmin, IsSchoolAuthorized])
    def delete_user(self, request):
        """Удаление пользователя по user_id. Так же при удалении пользователя удаляются и его токены авторизации"""
        serializers = TokenSerializer(data=request.data)
        if serializers.is_valid():
            user = SchoolUser.objects.filter(user_id=serializers.data["user_id"]).delete()
            token = Token.objects.filter(user_id=serializers.data["user_id"]).delete()
            return Response({"success": "Данные удалены"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Не удалось найти пользователя по данному user_id"}, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(parser_classes=[MultiPartParser], request_body=SchoolSerializer)
    @action(detail=False, methods=["post"], serializer_class=SchoolSerializer, 
            permission_classes=[IsSchoolAdmin, IsSchoolAuthorized], parser_classes=[MultiPartParser])
    def create_user(self, request, *args, **kwargs):
        """Создает нового пользователя. Создавать пользователя может только администратор"""
        serializers = SchoolSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            user = SchoolUser.objects.get(username=serializers.data["username"])
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response({"error": "Некорректная форма передачи данных"}, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(parser_classes=[MultiPartParser], request_body=SchoolSerializer)
    @action(detail=False, methods=["put"], parser_classes=[MultiPartParser], 
            permission_classes=[IsSchoolAuthorized, IsSchoolAdmin], url_path="update_user/<user_id>")
    def update_user(self, request, *args, **kwargs):
        """Обновить данные пользователя"""
        user_id = kwargs.get("user_id", None)
        instance = SchoolUser.objects.get(user_id=user_id)
        serializers = SchoolSerializer(data=request.data, instance=instance)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_206_PARTIAL_CONTENT)
        return Response({"error": "Не удалось обновить данные"}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=["post"], serializer_class=TokenSerializer, permission_classes=[IsSchoolAuthorized])
    def get_token(self, request):
        """Возвращает токен выбранного пользователя по user_id. Получить могут только авторизованные пользователи"""
        serializers = TokenSerializer(data=request.data)
        if serializers.is_valid():
            token = Token.objects.get(user_id=serializers.data["user_id"])
            return Response(serializers.data, status=status.HTTP_202_ACCEPTED)
        return Response({"error": "Пользователь ранее был авторизован или его токен устарел"}, status=status.HTTP_400_BAD_REQUEST)
    

class TeacherApiViewSet(ListViewSet):
    """Пользователи, являющиеся учителями. Доступ ко всем учителям имеет только администратор"""
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsSchoolAuthorized, IsSchoolAdmin]
    parser_classes= [MultiPartParser]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(parser_classes=[MultiPartParser], request_body=TeacherSerializer)
    @action(detail=False, methods=["post"], serializer_class=TeacherSerializer, parser_classes=[MultiPartParser])
    def create_teacher(self, request):
        """Создать учителя на основе пользователя"""
        serializers = TeacherSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response({"error": "Некорректная форма передачи данных"}, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(parser_classes=[MultiPartParser], request_body=TeacherSerializer)
    @action(detail=False, methods=["put"], parser_classes=[MultiPartParser], 
            permission_classes=[IsSchoolAuthorized, IsSchoolAdmin], url_path="update_teacher/<teacher_id>")
    def update_teacher(self, request, *args, **kwargs):
        """Обновить основную информацию школьника"""
        teacher_id = kwargs.get("teacher_id", None)
        instance = Teacher.objects.get(teacher_id=teacher_id)
        serializers = TeacherSerializer(data=request.data, instance=instance)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response({"error": "Некорректная форма передачи данных"}, status=status.HTTP_400_BAD_REQUEST)

class PupilApiViewSet(CreateListViewSet):
    """Пользователи, являющиеся школьниками. Доступ ко всем школьникам имеет только администратор. Преподаватель получает только свой класс"""
    queryset = Pupil.objects.all()
    serializer_class = PipulSerializer
    permission_classes=[IsSchoolAuthorized, IsSchoolAdmin]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(parser_classes=[MultiPartParser], request_body=PipulSerializer)
    @action(detail=False, methods=["post"], serializer_class=PipulSerializer, 
            permission_classes=[IsSchoolAuthorized, IsSchoolAdmin], parser_classes=[MultiPartParser])
    def create_pupil(self, request):
        """Создать учителя на основе пользователя"""
        serializers = PipulSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response({"error": "Некорректная форма передачи данных"}, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(parser_classes=[MultiPartParser], request_body=PipulSerializer)
    @action(detail=False, methods=["put"], parser_classes=[MultiPartParser], serializer_class=PipulSerializer,
            permission_classes=[IsSchoolAuthorized, IsSchoolAdmin], url_path="update_pupil/<user_id>")
    def update_pupil(self, request, *args, **kwargs):
        user_id = kwargs.get("user_id", None)
        instance = Pupil.objects.get(user_id=user_id)
        serializers = PipulSerializer(data=request.data, instance=instance)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response({"error": "Некорректная форма передачи данных"}, status=status.HTTP_400_BAD_REQUEST)

class RulesApiViewSet(CreateListViewSet):
    """Правила. Пока непонятно, что это, но пусть работает"""
    queryset = Rules.objects.all()
    serializer_class = RulesSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
class CompetitionApiViewSet(ListViewSet):
    """Обработка конкурсов. К конкурсам относятся как школьные, так и для учителей"""
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=["post"], serializer_class=CompetitionSerializer)
    def create_competition(self, request):
        """Создать конкурс. Автор конкурса является только администратор, зарегестрировавший его"""
        return Response({}, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=["post"])
    def add_owners(self, request):
        """Добавить преподавательский состав для конкурса"""
        pass
    
    @action(detail=False, methods=["post"], serializer_class=CompetitionFileSerializer)
    def add_files(self, request):
        """Добавить файл в активный конкурс. В случае отсутствия конкурса или его неактивности файл добавить не получится"""
        serializers = CompetitionFileSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response({"error": "Некорректный запрос со стороны клиента"}, status=status.HTTP_400_BAD_REQUEST)
            
class CompetitionFilesApiViewSet(ListViewSet):
    """Хранилище файлов для определенных конкурсов"""
    queryset = CompetitionFiles.objects.all()
    serializer_class = CompetitionFileSerializer
    permission_classes = [AllowAny, IsSchoolAdmin, IsSchoolAuthorized]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(request_body=CompetitionFileSerializer)
    @action(detail=False, methods=["post"], serializer_class=CompetitionFileSerializer, parser_classes=[MultiPartParser])
    def create_file(self, request):
        if serializers.is_valid():
            return Response({}, status=status.HTTP_201_CREATED)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)

class ShopApiViewSet(CreateListViewSet):

    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminUser]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


    