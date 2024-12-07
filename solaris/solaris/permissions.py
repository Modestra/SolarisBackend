from rest_framework.permissions import BasePermission
from solaris.models import Token

class IsSchoolAdmin(BasePermission):
    """Проверяет, является ли пользователь школьным админом"""
    def has_permission(self, request, view):
        return bool(request.user.is_admin)

class IsSchoolAuthorized(BasePermission):
    """Проверяет наличие пользовательского токена в системе"""
    def has_permission(self, request, view):
        try:
            return Token.objects.filter(user_id=request.user.user_id).exists()
        except AttributeError: # У класса AnonymousUser нет переменной user_id. Костыль для обхода ограничения
            return False;