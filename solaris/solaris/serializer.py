from rest_framework import serializers
from solaris.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        field = ['login', 'register']

class AdminUserSerializer(serializers.ModelSerializer):
    """Регистрация пользователя администратором"""
    class Meta:
        model = Users
        field = ['login', 'register']

class FeedbackSerializer(serializers.ModelSerializer):
    """Форма заполнения для отзыва и предложений"""
    class Meta:
        model = FeedbackForm
        field = ['name', 'phone', 'email', 'description']