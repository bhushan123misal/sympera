# Generated by Django 5.1.1 on 2024-10-08 10:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_remove_customer_opening_amount_customer_balance_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(max_length=10, primary_key=True, serialize=False, validators=[django.core.validators.MinLengthValidator(10)]),
        ),
    ]
