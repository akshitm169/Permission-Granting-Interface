# Generated by Django 3.0.3 on 2020-04-29 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pgi_app', '0014_remove_authority_db_ub'),
    ]

    operations = [
        migrations.AddField(
            model_name='authority_db',
            name='ub',
            field=models.CharField(max_length=200, null=True),
        ),
    ]