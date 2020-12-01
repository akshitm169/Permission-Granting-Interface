# Generated by Django 3.0.3 on 2020-04-23 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pgi_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authority_db',
            name='club',
            field=models.CharField(choices=[('Computer Science Society', 'Computer Science Society'), ('Art and Photography Club', 'Art and Photography Club'), ('Dramatics Club', 'Dramatics Club'), ('Not Valid', 'Not Valid')], max_length=200, null=True),
        ),
    ]
