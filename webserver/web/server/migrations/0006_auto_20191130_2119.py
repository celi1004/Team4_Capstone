# Generated by Django 2.1.7 on 2019-11-30 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0005_auto_20191128_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='number',
            field=models.CharField(max_length=50),
        ),
    ]
