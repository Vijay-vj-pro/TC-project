# Generated by Django 4.2.6 on 2024-09-08 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datab',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
    ]
