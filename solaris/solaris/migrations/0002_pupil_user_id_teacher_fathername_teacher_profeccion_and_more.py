# Generated by Django 4.1 on 2024-12-07 07:53

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('solaris', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pupil',
            name='user_id',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AddField(
            model_name='teacher',
            name='fathername',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='profeccion',
            field=models.CharField(choices=[('Русский язык', 'Русский язык'), ('Литература', 'Литература'), ('Математика', 'Математика'), ('Свободен', 'Свободен')], default='Свободен', max_length=255),
        ),
        migrations.AddField(
            model_name='teacher',
            name='user_id',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='competition_activities',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='token',
            name='update_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 7, 14, 53, 46, 339075)),
        ),
    ]