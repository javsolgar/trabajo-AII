# Generated by Django 3.1.2 on 2021-01-15 13:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0002_auto_20210112_1915'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perfil',
            name='intereses',
        ),
    ]
