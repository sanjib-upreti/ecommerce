# Generated by Django 2.2.6 on 2019-11-30 18:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_testproduct_brand'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testproduct',
            name='brand',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='products.Brand'),
        ),
    ]
