# Generated by Django 4.2.6 on 2024-09-20 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_datab2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datab2',
            name='year',
            field=models.IntegerField(),
        ),
    ]
