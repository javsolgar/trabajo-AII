# Generated by Django 3.1.2 on 2021-01-12 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommendation', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='puntuacion',
            old_name='puntuaciones',
            new_name='juego',
        ),
        migrations.RenameField(
            model_name='puntuacion',
            old_name='usuario',
            new_name='perfil',
        ),
        migrations.AddField(
            model_name='puntuacion',
            name='valor',
            field=models.IntegerField(default=0),
        ),
    ]
