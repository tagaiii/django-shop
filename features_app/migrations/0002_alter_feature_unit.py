# Generated by Django 4.0.4 on 2022-05-23 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('features_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feature',
            name='unit',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Единица измерения'),
        ),
    ]
