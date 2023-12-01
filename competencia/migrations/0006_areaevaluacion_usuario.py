
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_usuario_telefono'),
        ('competencia', '0005_delete_prueba_competencia_banner1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='areaevaluacion',
            name='usuario',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='Usuario', to='login.usuario'),
            preserve_default=False,
        ),
    ]
