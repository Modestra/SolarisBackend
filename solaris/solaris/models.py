from typing import Any
import uuid, jwt, datetime
from django.db import models
from django.conf import settings 
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin, AnonymousUser)
from rest_framework import exceptions

class UserManager(BaseUserManager):
    """Наследование логики с модели пользователя Django для кастомного пользователя"""

    def create_user(self, username, email, password=None):

        if username is None:
            raise TypeError("User не имеет имени")
        
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user
    
    def create_superuser(self, username, email, password):
        """ Создает и возввращет пользователя с привилегиями суперадмина. """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user
    
class SchoolUserManager(models.Manager):
    def create_admin(self, is_admin, **extra_fields):
        user = self.model(is_admin=True, **extra_fields)
        pass

class CategoryType(models.TextChoices):
    TEACHER = 'Учитель', 'Учитель'
    PUPIL = 'Ученик', 'Ученик'

class NotificationsType(models.TextChoices):
    SUCCESS = "Успешно", "Успешно"
    PROCESS = "В процессе", "В процессе"
    ERROR = "Отказано", "Отказано"
    NON_INFO = "Не подтверждён", "Не подтверждён"

class RoutesChoices(models.TextChoices):
    PATRIOT = "Патриотическое", "Патриотическое"
    INGENER = "Инженер", "Инженер"
    CHEMIST = "Химик", "Химик"
    BIOLOG = "Биолог", "Биолог"
    SPORT = "Спортсмен", "Спортсмен"

class ProfeccionChoices(models.TextChoices):
    PUSSIAN = "Русский язык", "Русский язык"
    LITERATURE = "Литература", "Литература"
    MATH = "Математика", "Математика"
    DEFAULT = "Свободен", "Свободен"

class Token(models.Model):
    """Токены авторизации пользователя. Если пользователь зарегестрирован, но не авторизован в системе, то пользователь получит отказ"""
    id = models.AutoField(primary_key=True)
    user_id = models.UUIDField()
    token = models.TextField()
    update_date = models.DateTimeField(default=datetime.datetime.now())

class User(AbstractBaseUser, PermissionsMixin):
    """Основная форма для пользователя, унаследованная от Django User. Является суперпользователем"""
    id = models.AutoField(primary_key=True)
    user_id = models.UUIDField(default=uuid.uuid4)

    email = models.EmailField(db_index=True, unique=True)
    username = models.CharField(db_index=True, max_length=255, unique=True)
    password = models.TextField()

    is_active = models.BooleanField(default=True)
    #Показывает, имеет ли пользователь доступ к админке
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #Поле, которое используется для аутентификации пользователя    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()
    school = SchoolUserManager()

    def __str__(self) -> str:
        return self.email
    
    @property
    def token(self):
        """Получение JWT токена путем вызова user.token"""
        return self._generate_jwt_token()
    
    def _generate_jwt_token(self):

        dt = datetime.datetime.now() + datetime.timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': 1000
        }, settings.SECRET_KEY, algorithm='HS256')

        return token
    
class SchoolUser(models.Model):
    """Форма школьного пользователя. Не имеет доступа к базе данных напрямую."""
    id = models.AutoField(primary_key=True)
    user_id = models.UUIDField(default=uuid.uuid4)
    email = models.EmailField(db_index=True, unique=True)
    username = models.CharField(db_index=True, max_length=255, unique=True)
    password = models.TextField()
    category = models.CharField(max_length=25, choices=CategoryType.choices, default=CategoryType.PUPIL)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = models.Manager()

    def __str__(self):
        return self.username
    
    @property
    def token(self):
        """Получение JWT токена путем вызова user.token"""
        return self._generate_jwt_token()
    
    def _generate_jwt_token(self):

        dt = datetime.datetime.now() + datetime.timedelta(days=1)

        token = jwt.encode({
            'id': self.pk, #Создается токен на основе Id созданного пользователя
            'exp': 99999999999
        }, settings.SECRET_KEY, algorithm='HS256')

        return token
    
    def is_token_olded(self, token):
        """Проверка старости токена. Не генерирует новый"""
        return self._is_token_olded(token)

    def _is_token_olded(token):
        pass

class Teacher(models.Model):
    """Основная модель для создания учителя. Создается только администратором"""
    id = models.AutoField(primary_key=True)
    user_id = models.UUIDField(default=uuid.uuid4)
    teacher_id = models.UUIDField(default=uuid.uuid4)
    name = models.TextField()
    surname = models.TextField()
    fathername = models.TextField(null=True)
    profeccion = models.CharField(max_length=255, choices=ProfeccionChoices.choices, default=ProfeccionChoices.DEFAULT)
    competition_activities = models.TextField(null=True)

    def __str__(self):
        return self.surname + self.name

class Pupil(models.Model):
    """Основная модель для создания школьника. Создается администратором"""
    id = models.AutoField(primary_key=True) # id
    name = models.TextField() #Имя
    surname = models.TextField() #Фамилия
    fathername = models.TextField(null=True)
    user_id = models.UUIDField(default=uuid.uuid4)
    class_name = models.CharField(max_length=5, default="1А")
    competition_activities = models.TextField(null=True) #Строка, которая указывает, в каких конкурсах участвует школьник
    shop_id = models.UUIDField(default=uuid.uuid4) #Идентификатор кошелька для магазина
    teacher_id = models.UUIDField(default=uuid.uuid4)

    def __str__(self):
        return self.name + self.surname

class FeedbackForm(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=25)
    description = models.TextField()

class Competition(models.Model):
    """Конкурсы. Основная информация"""
    id = models.AutoField(primary_key=True)
    competition_id = models.UUIDField(default=uuid.uuid4)
    name = models.CharField(max_length=255)
    description = models.TextField()
    goal_competition = models.TextField(null=True)
    tasks_compotition = models.TextField(null=True)
    author_id = models.UUIDField(null=False, default=uuid.uuid4)
    owners_id = models.TextField(null=False, default=uuid.uuid4)
    rules = models.CharField(max_length=255, null=False, default="Нет")

class CompetitionFiles(models.Model):
    """Конкурсные файлы. """
    id = models.AutoField(primary_key=True)
    competition_id = models.UUIDField()
    name = models.CharField(max_length=255)
    media = models.FileField(upload_to="media/", null=True, blank=True)
    
class Shop(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    cell = models.IntegerField()

class Rules(models.Model):
    id = models.AutoField(primary_key=True)
    rule = models.CharField(max_length=255)

class Notifications(models.Model):
    """Блок передачи уведомлений о данных изменений пользователя"""
    id = models.AutoField(primary_key=True)
    user_id = models.UUIDField()
    name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=255, choices=NotificationsType.choices, default="Не подтверждён")
    