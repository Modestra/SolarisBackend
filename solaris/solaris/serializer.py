from rest_framework import (serializers, viewsets)
from rest_framework.decorators import action
from django.contrib.auth.models import User
from solaris.models import *

class UserSerializer(viewsets.ModelViewSet):
    class Meta:
        model = User
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    """Форма заполнения для отзыва и предложений"""
    class Meta:
        model = FeedbackForm
        fields = '__all__'
        field = ['name', 'phone', 'email', 'description']