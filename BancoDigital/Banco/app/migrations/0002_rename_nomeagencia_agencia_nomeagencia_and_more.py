# Generated by Django 5.1.1 on 2024-09-20 18:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='agencia',
            old_name='nomeAgencia',
            new_name='nomeagencia',
        ),
        migrations.RenameField(
            model_name='agencia',
            old_name='numeroAgencia',
            new_name='numeroagencia',
        ),
    ]