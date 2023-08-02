# Generated by Django 4.0.4 on 2022-05-16 05:16

from django.db import migrations, models
import django.db.models.deletion
import mainapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_alter_cartitem_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to=mainapp.models.upload_image_function, verbose_name='Изображение смартфона'),
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to=mainapp.models.upload_image_function, verbose_name='Изображения')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.product', verbose_name='Смартфон')),
            ],
        ),
    ]