# Generated by Django 4.2.1 on 2023-05-21 12:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cloud', '0010_server_ips'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servers',
            name='server_os_version',
        ),
        migrations.AlterField(
            model_name='servers',
            name='server_ip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cloud.server_ips'),
        ),
        migrations.AlterField(
            model_name='servers',
            name='server_location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cloud.server_locations'),
        ),
        migrations.AlterField(
            model_name='servers',
            name='server_os',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cloud.server_os'),
        ),
    ]
