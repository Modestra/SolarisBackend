import jwt
from rest_framework.authentication import BaseAuthentication
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework import exceptions
from django.conf import settings
from django.contrib.auth import get_user_model
from solaris.models import User

class CSRFCheck(CsrfViewMiddleware):
    def _reject(self, request, reason):
        # Возвращается в случае некорректного HTTP запроса
        return reason

class SolarisJWTAuthentification(BaseAuthentication):
    """Логика для авторизации пользователей на основе кастомной модели solaris.User"""

    #Создание логики для авторизации
    def authenticate(self, request):
        
        UserModel = User
        authorization_header = request.headers.get('Authorization')

        if not authorization_header:
            return None
        try:
            access_token = authorization_header.split(' ')[1]
            user = User.objects.first()
        except(IndexError, User.DoesNotExist):
            raise exceptions.AuthenticationFailed('Некорректный Token')
        
        return (user, None)
    
    def enforce_csrf(self, request):
        """
        Enforce CSRF validation
        """
        check = CSRFCheck()
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        if reason:
            raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)
        