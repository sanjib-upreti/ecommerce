# Generated by Django 2.2.6 on 2019-10-11 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testproduct',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=15),
        ),
    ]
