# Generated by Django 3.1.2 on 2021-01-12 18:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='perfil',
            old_name='user',
            new_name='usuario',
        ),
    ]
