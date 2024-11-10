import jwt
from rest_framework.authentication import BaseAuthentication
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework import exceptions
from django.conf import settings
from django.contrib.auth import get_user_model
from solaris.models import SchoolUser

class CSRFCheck(CsrfViewMiddleware):
    def _reject(self, request, reason):
        # Возвращается в случае некорректного HTTP запроса
        return reason

class SolarisJWTAuthentification(BaseAuthentication):
    """Логика для авторизации пользователей на основе кастомной модели solaris.User"""

    #Создание логики для авторизации
    def authenticate(self, request):
        

        request.user = None

        authorization_header = request.headers.get('Authorization')

        if not authorization_header:
            return None
        try:
            access_token = authorization_header.split(' ')[0]
        except(IndexError):
            raise exceptions.AuthenticationFailed('Некорректный Token')
        
        return self._authenticate_credentials(request, access_token)
    
    def _authenticate_credentials(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY) #Далее здесь токен декодируется, но вызывает ошибку
        except Exception:
            msg = 'Ошибка аутентификации. Невозможно декодировать токен'
            raise exceptions.AuthenticationFailed(msg)
        try:
            #Доделать
            #Стоит ли проверять на данном уровне является ли пользовать админом?
            user = SchoolUser.objects.get(pk=payload['id']) #Потом в последствии декодинга получаем пользователя по id
        except SchoolUser.DoesNotExist:
            msg = 'Пользователь соответствующий данному токену не найден.'
            raise exceptions.AuthenticationFailed(msg)
        
        return (user, token)
    
    def enforce_csrf(self, request):
        """
        Enforce CSRF validation
        """
        check = CSRFCheck()
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        if reason:
            raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)
    
        