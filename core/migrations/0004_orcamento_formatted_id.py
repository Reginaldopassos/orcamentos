# Generated by Django 4.2.15 on 2024-08-28 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_orcamento_formatted_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='orcamento',
            name='formatted_id',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
