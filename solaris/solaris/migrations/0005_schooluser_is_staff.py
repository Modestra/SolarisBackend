# Generated by Django 4.1 on 2024-11-24 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solaris', '0004_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='schooluser',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]
