# Generated by Django 4.2.6 on 2024-09-20 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_datab_jn_datab_my_datab_sn_datab_vn'),
    ]

    operations = [
        migrations.CreateModel(
            name='datab2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(max_length=225)),
                ('pdf', models.FileField(upload_to='pdfs/')),
            ],
        ),
    ]
