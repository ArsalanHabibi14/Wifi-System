# Generated by Django 3.2.14 on 2022-09-30 12:12

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_auto_20220930_1618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
