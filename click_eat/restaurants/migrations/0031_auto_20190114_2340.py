# Generated by Django 2.1.2 on 2019-01-14 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0030_restaurant_inforate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='infoRate',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]