# Generated by Django 2.1.2 on 2019-01-14 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0025_auto_20190114_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='rate',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
