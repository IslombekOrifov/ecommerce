# Generated by Django 3.2 on 2022-11-08 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0002_auto_20221107_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]