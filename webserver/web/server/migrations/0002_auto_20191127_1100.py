# Generated by Django 2.1.7 on 2019-11-27 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='server',
            old_name='title',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='server',
            old_name='body',
            new_name='keyword',
        ),
        migrations.AddField(
            model_name='server',
            name='number',
            field=models.TextField(default='you'),
        ),
    ]
