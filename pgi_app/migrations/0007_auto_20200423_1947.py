# Generated by Django 3.0.3 on 2020-04-23 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pgi_app', '0006_auto_20200423_1946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room_db',
            name='room_number',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
