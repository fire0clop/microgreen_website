# Generated by Django 4.2.4 on 2023-09-12 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordering', '0002_order_company_name_order_delivery_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateField(),
        ),
    ]
