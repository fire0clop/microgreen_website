# Generated by Django 4.2.4 on 2023-09-14 03:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myaccount', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='email',
            new_name='company_name',
        ),
    ]
