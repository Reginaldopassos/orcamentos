# Generated by Django 4.2.15 on 2024-08-24 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orcamento',
            name='formatted_id',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]
