# Generated by Django 5.1.1 on 2024-10-03 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_transacao_contadestino'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transacao',
            name='status',
            field=models.CharField(default='pendente', editable=False, max_length=20, verbose_name='Status'),
        ),
    ]
