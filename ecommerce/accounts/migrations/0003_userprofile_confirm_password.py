# Generated by Django 2.2.6 on 2019-11-19 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_guestemail'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='confirm_password',
            field=models.CharField(default='123456', max_length=20),
            preserve_default=False,
        ),
    ]
