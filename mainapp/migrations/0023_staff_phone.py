# Generated by Django 4.0.4 on 2022-05-26 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0022_alter_product_features'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='phone',
            field=models.CharField(default=12, max_length=25, verbose_name='Номер телефона'),
            preserve_default=False,
        ),
    ]