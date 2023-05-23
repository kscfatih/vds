# Generated by Django 4.2.1 on 2023-05-19 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloud', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='server_packages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package_name', models.CharField(max_length=255)),
                ('package_cpu', models.CharField(max_length=255)),
                ('package_ram', models.CharField(max_length=255)),
                ('package_disk', models.CharField(max_length=255)),
                ('package_price', models.CharField(max_length=255)),
                ('package_transfer_limit', models.CharField(max_length=255)),
            ],
        ),
    ]
