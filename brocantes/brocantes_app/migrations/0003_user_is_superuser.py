# Generated by Django 5.0.7 on 2024-09-09 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brocantes_app', '0002_user_is_active_user_is_staff_user_last_login_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]