# Generated by Django 4.2.6 on 2023-11-27 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competencia', '0009_remove_inscripcion_competencia_codigo_carro_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competencia',
            name='banner1',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='competencia',
            name='banner2',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='competencia',
            name='banner3',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
