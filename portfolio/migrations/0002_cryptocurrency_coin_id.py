# Generated by Django 5.0.2 on 2025-03-13 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cryptocurrency',
            name='coin_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
