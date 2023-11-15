# Generated by Django 4.2.6 on 2023-11-15 21:33

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NombreCategoria', models.CharField(max_length=60)),
                ('DescipcionCategoria', models.CharField(max_length=250)),
                ('EstadoCategoria', models.CharField(default='Disponible', max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Competencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NombreCompetencia', models.CharField(max_length=60)),
                ('DescipcionCompetencia', models.CharField(max_length=250)),
                ('LugarCompetencia', models.CharField(max_length=150)),
                ('FechaCompetencia', models.DateField(default=datetime.date.today)),
                ('FechaLimiteInscripcion', models.DateField(default=datetime.date.today)),
                ('FechaLimiteActualizarDatos', models.DateField(default=datetime.date.today)),
                ('EstadoCompetencia', models.CharField(default='Disponible', max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Regla',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NombreRegla', models.CharField(max_length=60)),
                ('DescipcionRegla', models.CharField(max_length=250)),
                ('EstadoRegla', models.CharField(default='Disponible', max_length=60)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Regla', to='competencia.categoria')),
            ],
        ),
        migrations.AddField(
            model_name='categoria',
            name='competencia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Categoria', to='competencia.competencia'),
        ),
        migrations.CreateModel(
            name='AreaEvaluacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NombreAreaEvaluacion', models.CharField(max_length=60)),
                ('DescipcionAreaEvaluacion', models.CharField(max_length=250)),
                ('EstadoAreaEvaluacion', models.CharField(default='Disponible', max_length=60)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='AreaEvaluacion', to='competencia.categoria')),
            ],
        ),
    ]