# Generated by Django 2.2.6 on 2019-10-12 17:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20191012_1643'),
    ]

    operations = [
        migrations.AddField(
            model_name='testproduct',
            name='discount',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(99), django.core.validators.MinValueValidator(0)]),
        ),
    ]
