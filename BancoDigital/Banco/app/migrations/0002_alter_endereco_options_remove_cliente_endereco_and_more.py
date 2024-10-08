# Generated by Django 5.1.1 on 2024-10-08 16:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='endereco',
            options={},
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='endereco',
        ),
        migrations.AddField(
            model_name='endereco',
            name='cliente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='enderecos', to='app.cliente'),
        ),
    ]
