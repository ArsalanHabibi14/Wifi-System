# Generated by Django 3.2.14 on 2022-09-30 11:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_files'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='files',
            name='admin_user',
        ),
        migrations.AddField(
            model_name='files',
            name='admin_wifi',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.wifi'),
        ),
    ]
