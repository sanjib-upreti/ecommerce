# Generated by Django 2.2.6 on 2019-10-14 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_testproduct_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='testproduct',
            name='slug',
            field=models.SlugField(blank=True, max_length=250, null=True),
        ),
    ]
