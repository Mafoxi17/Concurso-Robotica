# Generated by Django 4.2.6 on 2023-11-26 21:22

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_alter_usuario_tipo_usuario'),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NombreEquipo', models.CharField(max_length=60)),
                ('DescipcionEquipo', models.CharField(max_length=250)),
                ('EstadoEquipo', models.CharField(default='Activo', max_length=60)),
                ('fecha_registro', models.DateField(default=datetime.date.today)),
            ],
        ),
        migrations.CreateModel(
            name='ParticipantesEquipos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Estado_ParticipanteEquipo', models.CharField(default='Activo', max_length=60)),
                ('fecha_ParticipanteEquipo', models.DateField(default=datetime.date.today)),
                ('equipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ParticipantesEquipos', to='login.equipo')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ParticipantesUsuarios', to='login.usuario')),
            ],
        ),
    ]