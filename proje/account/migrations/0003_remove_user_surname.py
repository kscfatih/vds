# Generated by Django 4.2.1 on 2023-05-17 14:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_user_surname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='surname',
        ),
    ]
