# Generated by Django 3.0.3 on 2020-04-29 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pgi_app', '0016_auto_20200429_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authority_db',
            name='ub',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
