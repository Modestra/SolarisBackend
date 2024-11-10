from rest_framework import (serializers, viewsets)
from django.contrib.auth import authenticate
from rest_framework.decorators import action
from solaris.models import *
from django.contrib.auth import authenticate
import uuid

class AuthSerializer(serializers.Serializer):
    """Авторизация пользователя. Хранит информацию о токене, а так же о пользователе"""
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    
    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        if username is None:
            raise serializers.ValidationError("Поле username пусто или некорректно")
        
        if password is None:
            raise serializers.ValidationError("Поле password пусто или некорректно")
        
        return data
        
    def create(self, username, password):
        try:
            user = SchoolUser.objects.get(username=username, password=password)
            return user
        except SchoolUser.DoesNotExist:
            return serializers.ValidationError("Пользователь с такими данными не найден")

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

class SchoolSerializer(serializers.ModelSerializer):
    """Форма сериализации для создания пользователя проекта. Только для суперпользователя"""
    class Meta:
        model = SchoolUser
        fields = ['email', 'username', 'password', 'category', 'is_admin']

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