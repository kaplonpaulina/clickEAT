# Generated by Django 2.1.2 on 2018-12-18 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0017_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='created',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='updated',
            field=models.DateTimeField(),
        ),
    ]
