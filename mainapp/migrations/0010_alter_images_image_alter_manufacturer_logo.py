# Generated by Django 4.0.4 on 2022-05-16 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0009_alter_manufacturer_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='image',
            field=models.ImageField(blank=True, upload_to='catalog/', verbose_name='Изображения'),
        ),
        migrations.AlterField(
            model_name='manufacturer',
            name='logo',
            field=models.ImageField(upload_to='logos/', verbose_name='Лого производителя'),
        ),
    ]
