from rest_framework import (serializers, viewsets)
from rest_framework.decorators import action
from solaris.models import *

class AuthSerializer(serializers.ModelSerializer):
    """Авторизация пользователя"""
    class Meta:
        model = User
        fields = ['username', 'password']

class AdminUserSerializer(serializers.ModelSerializer):
    """Получение всех данных, если пользователь является администратором"""

class FeedbackSerializer(serializers.ModelSerializer):
    """Форма заполнения для отзыва и предложений"""
    class Meta:
        model = FeedbackForm
        fields = '__all__'
        field = ['name', 'phone', 'email', 'description']

class SchoolSerializer(serializers.ModelSerializer):
    """Форма сериализации для создания пользователя проекта. Только для суперпользователя"""
    class Meta:
        model = SchoolUser
        fields = ['email', 'username', 'password', 'category', 'is_admin']