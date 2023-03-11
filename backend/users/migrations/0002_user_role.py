# Generated by Django 3.2.18 on 2023-03-11 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('user', 'user'), ('user', 'anonymous'), ('admin', 'admin')], default='user', max_length=15, verbose_name='Роль пользователя'),
        ),
    ]
