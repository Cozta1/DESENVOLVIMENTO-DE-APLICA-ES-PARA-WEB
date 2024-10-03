# Generated by Django 5.1.1 on 2024-10-03 19:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificacao',
            name='conta',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.conta'),
        ),
        migrations.AddField(
            model_name='notificacao',
            name='mensagem',
            field=models.TextField(default='Notificação padrão'),
        ),
    ]