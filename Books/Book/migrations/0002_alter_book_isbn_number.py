# Generated by Django 4.2.2 on 2023-06-08 18:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Book', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='isbn_number',
            field=models.IntegerField(unique=True, validators=[django.core.validators.RegexValidator(message='ISBN must be 10 or 13 digits long.', regex='^\\d{10}$|^\\d{13}$')]),
        ),
    ]
