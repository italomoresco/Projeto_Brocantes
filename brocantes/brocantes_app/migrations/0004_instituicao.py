# Generated by Django 5.0.7 on 2024-09-09 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brocantes_app', '0003_user_is_superuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instituicao',
            fields=[
                ('codigo', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=255)),
                ('cidade', models.CharField(max_length=100)),
                ('estado', models.CharField(max_length=2)),
            ],
        ),
    ]
