# Generated by Django 4.2.4 on 2023-09-12 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordering', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='company_name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_date',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
