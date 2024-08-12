import uuid
from django.db import models

class Category(models.Model):
    """Форма для категорий"""
    category_id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=15)

    def __str__(self):
        return self.name
class Users(models.Model):
    """Основная форма для пользователя"""
    id = models.AutoField(primary_key=True)
    user_id = models.UUIDField(default=uuid.uuid4)
    login = models.TextField()
    password = models.TextField()
    category = models.ForeignKey(Category, to_field="category", on_delete=models.SET_DEFAULT, default="Ученик", db_constraint=True)
    date_seccion = models.CharField()
    
    def __str__(self):
        return self.name
    
class Pupil(models.Model):
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