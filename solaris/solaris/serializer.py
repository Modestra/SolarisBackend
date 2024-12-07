from rest_framework import (serializers, viewsets)
from django.contrib.auth import authenticate
from rest_framework.decorators import action
from solaris.models import *
from django.contrib.auth import authenticate
import uuid

class AuthSerializer(serializers.Serializer):
    """Авторизация пользователя. Хранит информацию о токене, а так же о пользователе"""
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128)
    
    def validate(self, data): #Пустые значения не передаются. Блокируются Swagger
        username = data.get('username', None)
        password = data.get('password', None)
        
        if not SchoolUser.objects.filter(username=username).exists() and not SchoolUser.objects.filter(password=password).exists():
            raise serializers.ValidationError("Пользователь с данным именем или паролем не найден")

        return data
        
    def create(self, validated_data):
        return super().create(validated_data)
    
class TokenSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=255)
    token = serializers.CharField(max_length=1000,read_only=True)
    update_time = serializers.DateTimeField(read_only=True)

    def validate(self, attrs):
        user_id = attrs.get('user_id', None)
        if SchoolUser.objects.filter(user_id=user_id).exists():
            return attrs
        return serializers.ValidationError("Токенов с данным user_id несуществует. Пользовать ранее не авторизовывался")
    def create(self, validated_data):
        """Создает новый токен для пользователя по user_id"""
        if Token.objects.filter(user_id=validated_data.data["user_id"]).exists():
            return Token.objects.filter(**validated_data)
    
    def update(self, instance, validated_data):
        instance.token = validated_data.get("token", instance.token)
        instance.save()
        return instance
    
class UserIdSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()

    def validate(self, data):
        user_id = data.get("user_id", None)
        if not SchoolUser.objects.filter(user_id=user_id).exists():
            raise serializers.ValidationError("Не удалось найти пользователя с данным id")
        return data

class AdminUserSerializer(serializers.Serializer):
    """Создание пользователей администратором внутри самого проекта. Не является суперпользователей"""
    email = serializers.EmailField()
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    category = serializers.ChoiceField(choices=CategoryType.choices)

    def create(self, validated_data):
        #Не проверяется уникальность email
        return SchoolUser.objects.create(**validated_data)

class FeedbackSerializer(serializers.ModelSerializer):
    """Форма заполнения для отзыва и предложений"""
    class Meta:
        model = FeedbackForm
        fields = '__all__'

class SchoolSerializer(serializers.Serializer):
    """Форма сериализации для создания пользователя проекта. Только для суперпользователя"""
    user_id = serializers.UUIDField(read_only=True)
    email = serializers.EmailField()
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=1000)
    category = serializers.ChoiceField(choices=CategoryType.choices)
    is_admin = serializers.BooleanField(read_only=True)

    def create(self, validated_data):
        return SchoolUser.objects.create(**validated_data)
    
class PipulSerializer(serializers.Serializer):
    """Форма регистрации школьника"""
    name = serializers.CharField(max_length=100)
    surname = serializers.CharField(max_length=100) 
    fathername = serializers.CharField(max_length=100)
    user_id = serializers.UUIDField()
    class_name = models.CharField(max_length=5, default="1А")
    competition_activities = models.TextField(null=True)
    shop_id = serializers.UUIDField(read_only=True)
    teacher_id = serializers.UUIDField()

    def validate(self, attrs):
        return super().validate(attrs)
    
    def create(self, validated_data):
        return Pupil.objects.create(**validated_data)
    
class TeacherSerializer(serializers.Serializer):
    """Форма регистрации учителя"""
    user_id = serializers.UUIDField(default=uuid.uuid4)
    teacher_id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(max_length=100)
    surname = serializers.CharField(max_length=100)
    fathername = serializers.CharField(max_length=100)
    profeccion = serializers.ChoiceField(choices=ProfeccionChoices.choices)
    competition_activities = serializers.CharField(max_length=25565, read_only=True)

    def validate(self, attrs):
        return super().validate(attrs)
    
    def create(self, validated_data):
        return Teacher.objects.create(**validated_data)

class RulesSerializer(serializers.ModelSerializer):
    """Форма каких-то правил"""
    class Meta:
        model = Rules
        fields = '__all__'

class CompetitionSerializer(serializers.ModelSerializer):
    """Форма для создания конкурса"""
    class Meta:
        model = Competition
        fields = '__all__'
        read_only_fields = ['competition_id']

class CompetitionFileSerializer(serializers.Serializer):
    """Форма для работы с файлами конкурсов"""
    competition_id = serializers.CharField(max_length=255, read_only=True)
    media = models.FileField()

    def validate(self, attrs):
        return super().validate(attrs)
    
    def create(self, validated_data):
        return CompetitionFiles.objects.create(**validated_data)
    
#Добавить новые сериалайзеры для конкурсов

class ShopSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shop
        fields = '__all__'