# Generated by Django 4.2.4 on 2023-09-05 01:45

from django.db import migrations, models
import product.models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_alter_product_main_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='main_image',
            field=models.ImageField(upload_to=product.models.product_main_image),
        ),
    ]
