# Generated by Django 4.2.4 on 2023-09-12 05:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_alter_favoriteproduct_session_key'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FavoriteProduct',
        ),
    ]