# Generated by Django 5.1.1 on 2024-09-20 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_rename_nomeagencia_agencia_nomeagencia_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conta',
            name='numeroConta',
            field=models.CharField(blank=True, max_length=10, primary_key=True, serialize=False, unique=True),
        ),
    ]
