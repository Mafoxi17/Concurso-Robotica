# Generated by Django 4.2.6 on 2023-11-15 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competencia', '0003_alter_areaevaluacion_porcentaje'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prueba',
            name='banner1',
            field=models.BinaryField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='prueba',
            name='banner2',
            field=models.BinaryField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='prueba',
            name='banner3',
            field=models.BinaryField(blank=True, null=True),
        ),
    ]
