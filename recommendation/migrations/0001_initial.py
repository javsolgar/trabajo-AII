# Generated by Django 3.1.2 on 2021-01-10 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Desarrollador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Genero',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Juego',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.TextField()),
                ('url_juego', models.URLField()),
                ('url_imagen', models.URLField()),
                ('desarrollador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommendation.desarrollador')),
                ('generos', models.ManyToManyField(to='recommendation.Genero')),
            ],
        ),
        migrations.CreateModel(
            name='Jugadores',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jugadores', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Plataforma',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Puntuacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puntuaciones', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommendation.juego')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.perfil')),
            ],
        ),
        migrations.AddField(
            model_name='juego',
            name='jugadores',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommendation.jugadores'),
        ),
        migrations.AddField(
            model_name='juego',
            name='plataformas',
            field=models.ManyToManyField(to='recommendation.Plataforma'),
        ),
    ]
