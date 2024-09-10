import uuid, jwt, datetime
from django.db import models
from django.conf import settings 
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)

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

class CategoryType(models.TextChoices):
    ADMIN = 'Администратор', 'Администратор'
    TEACHER = 'Учитель', 'Учитель'
    PUPIL = 'Ученик', 'Ученик'

class User(AbstractBaseUser, PermissionsMixin):
    """Основная форма для пользователя, унаследованная от Django User"""
    id = models.AutoField(primary_key=True)
    user_id = models.UUIDField(default=uuid.uuid4)

    email = models.EmailField(db_index=True, unique=True)
    username = models.CharField(db_index=True, max_length=255, unique=True)
    password = models.TextField()

    category = models.CharField(max_length=25, choices=CategoryType.choices, default=CategoryType.PUPIL)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #Поле, которое используется для аутентификации пользователя    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

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
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')
    

class Pupil(models.Model):
    """Основная модель для создания школьника. Создается учителем или администратором"""
    id = models.AutoField(primary_key=True) # id
    name = models.TextField() #Имя
    surname = models.TextField() #Фамилия
    teacher_id = models.UUIDField(default= uuid.uuid4) #id, привязывающая к учителю. У учителя значение равно None

class FeedbackForm(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=25)
    description = models.TextField()