# Generated by Django 2.2.6 on 2019-10-12 07:19

from django.db import migrations, models
import django.db.models.deletion
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20191011_1847'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoryname', models.CharField(max_length=80, unique=True)),
                ('categoryimage', models.ImageField(blank=True, null=True, upload_to=products.models.upload_category_image_path)),
            ],
        ),
        migrations.AlterField(
            model_name='testproduct',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to=products.models.upload_image_path),
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subcategoryname', models.CharField(max_length=30)),
                ('subcategoryimage', models.ImageField(blank=True, null=True, upload_to=products.models.upload_subcategory_image_path)),
                ('categoryname', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Category')),
            ],
        ),
    ]
