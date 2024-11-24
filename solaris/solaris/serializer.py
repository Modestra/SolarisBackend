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

    def create(self, validated_data):
        """Создает новый токен для пользователя по user_id"""
        return Token.objects.create(**validated_data, update_date=datetime.datetime.now())
    
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
    class_name = serializers.CharField(max_length=3)

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

class RulesSerializer(serializers.ModelSerializer):
    """Форма заполнения для отзыва и предложений"""
    class Meta:
        model = Rules
        fields = '__all__'

class CompetitionSerializer(serializers.ModelSerializer):
    """Форма заполнения для отзыва и предложений"""
    class Meta:
        model = Competition
        fields = '__all__'
        read_only_fields = ['competition_id']

class CompetitionFileSerializer(serializers.ModelSerializer):
    """Форма заполнения для отзыва и предложений"""
    class Meta:
        model = CompetitionFiles
        fields = '__all__'

class ShopSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shop
        fields = '__all__'